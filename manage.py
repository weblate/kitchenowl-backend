from os import listdir
from os.path import isfile, join
import blurhash
from PIL import Image
from app import app, db
from app.config import UPLOAD_FOLDER
from app.jobs import jobs
from app.models import User, File, Household, HouseholdMember
from app.service.delete_unused import deleteEmptyHouseholds, deleteUnusedFiles


def importFiles():
    try:
        filesInUploadFolder = [f for f in listdir(UPLOAD_FOLDER) if isfile(join(UPLOAD_FOLDER, f))]
        def createFile(filename: str) -> File:
            blur = None
            try:
                with Image.open(join(UPLOAD_FOLDER, filename)) as image:
                    image.thumbnail((100, 100))
                    blur = blurhash.encode(
                        image, x_components=4, y_components=3)
            except FileNotFoundError:
                pass
            except Exception:
                pass
            return File(filename=filename, blur_hash=blur)
        files = [createFile(f) for f in filesInUploadFolder if not File.find(f)]

        db.session.bulk_save_objects(files)
        db.session.commit()
        print(f"-> Found {len(files)} new files in {UPLOAD_FOLDER}")
    except Exception as e:
        db.session.rollback()
        raise e

def manageHouseholds():
    while True:
        print("""
What next?
    1. List all households
    2. Delete empty
    (q) Go back""")
        selection = input("Your selection (q):")
        if selection == "1":
            for h in Household.all():
                print(f"Id {h.id}: {h.name} ({len(h.member)} members)")
        if selection == "2":
            print(f"Deleted {deleteEmptyHouseholds()} unused households")
        else:
            return

def manageUsers():
    while True:
        print("""
What next?
    1. List all users
    2. Update user
    3. Delete user
    (q) Go back""")
        selection = input("Your selection (q):")
        if selection == "1":
            for u in User.all():
                print(f"@{u.username} ({u.email}): {u.name} (server admin: {u.admin})")
        elif selection == "2":
            username = input("Enter the username:")
            user = User.find_by_username(username)
            if not user:
                print("No user found with that username")
            else:
                updateUser(user)
        elif selection == "3":
            username = input("Enter the username:")
            user = User.find_by_username(username)
            if not user:
                print("No user found with that username")
            else:
                user.delete()
        else:
            return

def updateUser(user: User):
        print(f"""
Settings for {user.name} (@{user.username}) (server admin: {user.admin})
    1. Update password
    2. Add to household
    3. Set server admin
    (q) Go back""")
        selection = input("Your selection (q):")
        if selection == "1":
            newPW = input("Enter new password:")
            if not newPW.strip(): 
                print("Password cannot be empty")
            newPWRepeat = input("Repeat new password:")
            if newPW.strip() == newPWRepeat.strip():
                user.set_password(newPW.strip())
                user.save()
            else:
                print("Passwords do not match")
        elif selection == "2":
            id = input("Enter the household id:")
            household = Household.find_by_id(id)
            if not household:
                print("No household found with that id")
            elif not HouseholdMember.find_by_ids(household.id, user.id):
                hm = HouseholdMember()
                hm.user_id = user.id
                hm.household_id = household.id
                hm.save()
            else:
                print("User is already part of that household")
        elif selection == "3":
            selection = input("Set admin (y/N):")
            user.admin = selection == "y"
            user.save()
        else:
            return

def manageFiles():
    while True:
        print("""
What next?
    1. Import files
    2. Delete unused files
    (q) Go back""")
        selection = input("Your selection (q):")
        if selection == "1":
            importFiles()
        elif selection == "2":
            print(f"Deleted {deleteUnusedFiles()} unused files")
        else:
            return

# docker exec -it [backend container name] python manage.py
if __name__ == "__main__":
    while True:
        print("""
Manage KitchenOwl\n---\nWhat do you want to do?
1.  Manage users
2.  Manage households
3.  Manage images/files
4.  Run all jobs
(q) Exit""")
        selection = input("Your selection (q):")
        if selection == "1":
            with app.app_context():
                manageUsers()
        elif selection == "2":
            with app.app_context():
                manageHouseholds()
        elif selection == "3":
            with app.app_context():
                manageFiles()
        elif selection == "4":
            print("Starting jobs (might take a while)...")
            jobs.daily()
            jobs.halfHourly()
            print("Done!")
        else:
            exit()

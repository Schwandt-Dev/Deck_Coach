from git import Repo

# Path to your local git repository
repo_path = r"C:/dev/Deck_Coach/"


def check_for_updates():
    repo = Repo(repo_path)
    origin = repo.remotes.origin

    # Fetch latest info from GitHub (does NOT modify local files)
    origin.fetch("main")

    local_commit = repo.commit("main")
    remote_commit = repo.commit("origin/main")

    if local_commit.hexsha != remote_commit.hexsha:
        print("\nA new update is available!")
        choice = input("Would you like to update now? (y/n): ").strip().lower()

        if choice == "y":
            print("Updating...")
            origin.pull("main")
            print("Update complete! Restart application to apply changes\n")
            exit(0)
        else:
            print("Skipping update.\n")
    else:
        print("Your application is already up-to-date.\n")



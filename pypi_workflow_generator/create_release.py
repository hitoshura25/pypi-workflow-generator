import argparse
import subprocess
import sys

def create_release_tag(version):
    try:
        # Create the git tag
        print(f"Creating git tag: {version}")
        subprocess.run(['git', 'tag', version], check=True)

        # Push the tag to the remote repository
        print(f"Pushing git tag: {version}")
        subprocess.run(['git', 'push', 'origin', version], check=True)

        print(f"Successfully created and pushed tag {version}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating or pushing tag: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: git command not found. Please ensure Git is installed and in your PATH.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Create and push a git version tag.')
    parser.add_argument('version', help='The version string for the tag (e.g., v1.0.0).')
    args = parser.parse_args()

    create_release_tag(args.version)

if __name__ == "__main__":
    main()

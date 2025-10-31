import argparse
import subprocess
import sys

def create_release_tag(version, overwrite=False):
    tag_exists = False
    try:
        # Check if the tag already exists
        subprocess.run(['git', 'rev-parse', version], check=True, capture_output=True)
        tag_exists = True
    except subprocess.CalledProcessError:
        # The tag does not exist, so we can proceed
        pass

    if tag_exists:
        if overwrite:
            print(f"Tag {version} already exists. Overwriting.")
            try:
                subprocess.run(['git', 'tag', '-d', version], check=True)
                try:
                    subprocess.run(['git', 'push', 'origin', ':' + version], check=True)
                except subprocess.CalledProcessError:
                    # The remote tag does not exist, which is fine
                    pass
            except subprocess.CalledProcessError as e:
                print(f"Error deleting tag: {e}")
                sys.exit(1)
        else:
            print(f"Error: Tag {version} already exists. Use --overwrite to replace it.")
            sys.exit(1)


    try:
        # Create the git tag
        print(f"Creating git tag: {version}")
        subprocess.run(['git', 'tag', version], check=True)

        print(f"Successfully created tag {version}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating or pushing tag: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: git command not found. Please ensure Git is installed and in your PATH.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Create and push a git version tag.')
    parser.add_argument('release_type', choices=['major', 'minor', 'patch'], help='The type of release (major, minor, or patch).')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite an existing tag.')
    args = parser.parse_args()

    try:
        latest_tag = subprocess.run(['git', 'describe', '--tags', '--abbrev=0'], check=True, capture_output=True, text=True).stdout.strip()
        major, minor, patch = map(int, latest_tag.lstrip('v').split('.'))
    except (subprocess.CalledProcessError, ValueError):
        major, minor, patch = 0, 0, 0

    if args.release_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif args.release_type == 'minor':
        minor += 1
        patch = 0
    elif args.release_type == 'patch':
        patch += 1

    new_version = f'v{major}.{minor}.{patch}'

    create_release_tag(new_version, args.overwrite)

if __name__ == "__main__":
    main()

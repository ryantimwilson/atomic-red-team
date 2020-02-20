import argparse
import os
import subprocess
import sys
import yaml

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--list', default=False, action="store_true")
    args = parser.parse_args()

    rootdir = "/Users/ryantimwilson/code/atomic-red-team/atomics"
    for d, _, filenames in os.walk(rootdir):
        for filename in filenames:
            if not filename.endswith(".yaml") or not filename.startswith("T"):
                continue
            (technique, names) = parse_file(os.path.join(d, filename))
            for name in names:
                if args.list:
                    print(technique + "," + name)
                else:
                    args = ["/usr/bin/ruby", "execution-frameworks/ruby/go-atomic.rb", "-t", technique, "-n", name]
                    # Some tests, like T1496, run infinitely...lets run it for 30 seconds, then move on
                    try:
                        subprocess.run(args, timeout=30, check=True)
                    except subprocess.TimeoutExpired:
                        pass

def parse_file(filename):
    with open(filename, "r") as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(e)
            sys.exit(1)
    technique = data["attack_technique"]
    names = []
    for test in data["atomic_tests"]:
        if "macos" in test["supported_platforms"] and test["executor"]["name"] != "manual":
            names.append(test["name"])
    return (technique, names)

if __name__ == "__main__":
    main()

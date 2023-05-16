import git

lesson_name = "dsc-functions-with-arguments-lab"

repo = f'https://github.com/learn-co-curriculum/{lesson_name}'

repo = git.Repo(repo)

repo.remotes.origin.pull()
repository = "/home/bart/tmp/restic"

directories = [
    "/home/bart/tmp/invalid",
    "/home/bart/tmp/test",
    "/home/bart/tmp/test2",
]

backup_args = []

prune_args = ["--keep-last", "5", 
              "--keep-hourly", "3",
              "--keep-daily", "1",
              "--keep-weekly", "4",
              "--keep-monthly", "3"]

# check_args = []
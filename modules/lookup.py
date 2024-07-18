import csv

def starLookup(file_path, target_id):
    with open(file_path, 'r') as file:
        file.seek(0, 2)
        filesize = file.tell()
        low, high = 0, filesize

        while low <= high:
            mid = (low + high) // 2
            file.seek(mid)
            file.readline()
            line = file.readline().strip()

            if not line:
                break

            current_id = line.split(',')[0]

            if current_id == target_id:
                return line
            elif current_id < target_id:
                low = mid + 1
            else:
                high = mid - 1

        return None


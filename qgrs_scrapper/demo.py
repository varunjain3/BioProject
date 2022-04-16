from utility import get_QGRS_data

if __name__ == "__main__":
    ref_id = input("Enter NCBI Ref ID: ")
    a = get_QGRS_data(ref_id)
    for key, value in a.items():
        print(f"{key}: {value}")
    
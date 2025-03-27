def add(*nums:int):
    res = sum(nums)

    # obviously wrong, needs patching
    return res + 1
    
def main():
    res = add(1,2)
    assert res==3

if __name__ == "__main__":
    main()
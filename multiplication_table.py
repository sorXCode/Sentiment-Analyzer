def multiples(root=2, term=12):
    '''
    Simple Multiplication chart to aid beginners
    learning arithmetics
    '''
    for x in range(root,term+1):
        for y in range(root, term+1):
            print(f"{y} x {x} = {y*x}", end='\t')
            if y==12:
                print("-"*5)

if __name__ == "__main__":
    multiples()
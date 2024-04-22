from ete3 import Tree

def main():
    tree = Tree('(((((Ailuropoda melanoleuca, Canis lupus), Felis catus), ((Ovis aries, Bos taurus), Sus scrofa)), ((Pan paniscus, Homo sapiens), Gorilla gorilla gorilla) ), Gallus gallus);')
    tree.show()

if __name__ == '__main__':
    main()

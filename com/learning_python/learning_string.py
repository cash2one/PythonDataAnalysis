__author__ = 'Zealot'


def main():
    a = 1
    b = 2
    x = a + b
    print x

    imperative = "abc"
    expletive = "123"
    s = '%s, %s!' % (imperative, expletive)
    print s
    x = '{}, {}!'.format(imperative, expletive)
    print x
    name = "eminem"
    n = 1
    s2 = 'name: %s; score: %d' % (name, n)
    print s2
    s3 = 'name: {}; score: {}'.format(name, n)
    print s3
    s4 = 'name: ' + name + '; score: ' + str(n)
    print s4

if __name__ == '__main__':
    main()
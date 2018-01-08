from datarefinery.CombineOperations import parallel, secuential


def test_emtpy():
    op_p = parallel(None)
    op_s = secuential(None)

    (res_p, err_p) = op_p(None)
    (res_s, err_s) = op_s(None)

    assert res_p == res_s == {}
    assert err_p == err_s == {}


def test_one_opertaion():
    def one_op(i, e):
        i.update({"hello": "Tom"})
        return i, e

    op_p = parallel(one_op)
    op_s = secuential(one_op)

    inp = {"hello": "world"}

    (res_p, err_p) = op_p(inp)

    assert inp == {"hello": "world"}

    (res_s, err_s) = op_s(inp)

    assert res_p == {"hello": "Tom"}
    assert res_s == {"hello": "Tom"}
    assert err_p == err_s == {}


def test_two_operations_parallel():
    def add_field(i, e):
        return {"who": "Tom"}, e

    def change_field(i, e):
        return {"hello": "Tom"}, e

    op_p = parallel(change_field, add_field)

    inp = {"hello": "world"}

    (res_p, err_p) = op_p(inp)

    assert inp == {"hello": "world"}
    assert res_p == {"who": "Tom", "hello": "Tom"}
    assert err_p == {}


def test_two_operations_sequential():
    def add_field(i, e):
        i.update({"who": "Tom"})
        return i, e

    def change_field(i, e):
        return "{} {}".format(i["greet"], i["who"]), e

    op_p = secuential(add_field, change_field)

    inp = {"greet": "hello"}

    (res_p, err_p) = op_p(inp)

    assert inp == {"greet": "hello"}
    assert res_p == "hello Tom"
    assert err_p == {}
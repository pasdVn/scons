#!/usr/bin/env python
#
# __COPYRIGHT__
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__revision__ = "__FILE__ __REVISION__ __DATE__ __DEVELOPER__"

import TestSCons

_python_ = TestSCons._python_

test = TestSCons.TestSCons()



test.write('myfc.py', r"""
import sys
fline = '#'+sys.argv[1]+'\n'
outfile = open(sys.argv[2], 'wb')
infile = open(sys.argv[3], 'rb')
for l in filter(lambda l, fl=fline: l != fl, infile.readlines()):
    outfile.write(l)
sys.exit(0)
""")

if not TestSCons.case_sensitive_suffixes('.f','.F'):
    f77pp = 'f77'
else:
    f77pp = 'f77pp'


test.write('SConstruct', """
env = Environment(F77COM = r'%(_python_)s myfc.py f77 $TARGET $SOURCES',
                  F77COMSTR = 'Building f77 $TARGET from $SOURCES',
                  F77PPCOM = r'%(_python_)s myfc.py f77pp $TARGET $SOURCES',
                  F77PPCOMSTR = 'Building f77pp $TARGET from $SOURCES',
                  OBJSUFFIX='.obj')
env.Object(source = 'test09.f77')
env.Object(source = 'test10.F77')
""" % locals())

test.write('test09.f77',        "A .f77 file.\n#f77\n")
test.write('test10.F77',        "A .F77 file.\n#%s\n" % f77pp)

test.run(stdout = test.wrap_stdout("""\
Building f77 test09.obj from test09.f77
Building %(f77pp)s test10.obj from test10.F77
""" % locals()))

test.must_match('test09.obj', "A .f77 file.\n")
test.must_match('test10.obj', "A .F77 file.\n")

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:

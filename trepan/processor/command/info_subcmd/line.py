# -*- coding: utf-8 -*-
#   Copyright (C) 2008-2009, 2013, 2015, 2020 Rocky Bernstein <rocky@gnu.org>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
import inspect, re
import os.path as osp

# Our local modules
from trepan.processor.command.base_subcmd import DebuggerSubcommand
from trepan.clifns import search_file
from trepan.misc import wrapped_lines
from trepan.processor.cmdbreak import parse_break_cmd
from pyficache import code_line_info


def find_function(funcname, filename):
    cre = re.compile(r"def\s+%s\s*[(]" % re.escape(funcname))
    try:
        fp = open(filename)
    except IOError:
        return None
    # consumer of this info expects the first line to be 1
    lineno = 1
    answer = None
    while True:
        line = fp.readline()
        if line == "":
            break
        if cre.match(line):
            answer = funcname, filename, lineno
            break
        lineno = lineno + 1
        pass
    fp.close()
    return answer


class InfoLine(DebuggerSubcommand):
    """**info line* [*location*]

Show information about the current line.

See also:
---------
`info program`, `info frame`"""

    min_abbrev = 2
    max_args = 4
    need_stack = False
    short_help = "Show line information"

    def lineinfo(self, arg):
        (func, filename, lineno, condition) = parse_break_cmd(self.proc, ["info args"])
        if filename != None and lineno != None:
            return lineno, filename
        else:
            return None, None

    def run(self, args):
        """Current line number in source file"""
        if not self.proc.curframe:
            self.errmsg("No line number information available.")
            return

        # info line <loc>
        if len(args) == 0:
            # No line number. Use current frame line number
            line_number = inspect.getlineno(self.proc.curframe)
            filename = self.core.canonic_filename(self.proc.curframe)
        elif len(args) == 1:
            # lineinfo returns (item, file, lineno) or (None,)
            line_number, filename = self.lineinfo(args[2:])
            if not filename:
                self.errmsg("Can't parse '%s'" % args[2])
                pass
            filename = self.core.canonic(filename)
        else:
            self.errmsg("Wrong number of arguments.")
            return
        if not osp.isfile(filename):
            filename = search_file(filename, self.core.search_path, self.main_dirname)
            pass

        line_info = code_line_info(filename, line_number)
        msg1 = 'Line %d of "%s"' % (line_number, self.core.filename(filename),)
        if line_info:
            msg2 = "starts at offset %d of %s and contains %d instructions" % (
                line_info[0].offsets[0],
                line_info[0].name,
                len(line_info[0].offsets),
            )
        self.msg(wrapped_lines(msg1, msg2, self.settings["width"]))
        if line_info and len(line_info) > 1:
            self.msg(
                "There are multiple starting offsets this line. Other starting offsets: %s"
                % ", ".join([str(li.offsets[0]) for li in line_info[1:]])
            )
        return False

    pass


if __name__ == "__main__":
    from trepan.processor.command import mock
    from trepan.processor.command.info import InfoCommand
    from trepan.debugger import Trepan

    d = Trepan()
    d, cp = mock.dbg_setup(d)
    i = InfoCommand(cp)
    sub = InfoLine(i)
    cp.curframe = inspect.currentframe()
    for width in (80, 200):
        sub.settings["width"] = width
        sub.run([])
        line = inspect.getlineno(cp.curframe); x = 1
        cp.current_command = "info args %d" % line
        sub.run([line])
        pass
    pass

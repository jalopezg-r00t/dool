global mysql_options
mysql_options = os.getenv('DSTAT_MYSQL')

class dstat_mysql_keys(dstat):
    def __init__(self):
        self.name = 'mysql key status'
        self.type = 'f'
        self.width = 4
        self.scale = 1000
        self.vars = ('Key_blocks_used', 'Key_reads', 'Key_writes', 'Key_read_requests', 'Key_write_requests')
        self.nick = ('used', 'read', 'writ', 'rreq', 'wreq')

    def check(self): 
        if not os.access('/usr/bin/mysql', os.X_OK):
            raise Exception, 'Needs MySQL binary'
        try:
            self.stdin, self.stdout, self.stderr = dpopen('/usr/bin/mysql -n %s' % mysql_options)
        except IOError:
            raise Exception, 'Cannot interface with MySQL binary'

    def extract(self):
        try:
            self.stdin.write("show status like 'Key_%';\n")
            for line in readpipe(self.stdout):
                l = line.split()
                if len(l) < 2: continue
                if l[0] in self.vars:
                    self.set2[l[0]] = float(l[1])

            for name in self.vars:
                self.val[name] = (self.set2[name] - self.set1[name]) * 1.0 / elapsed

            if step == op.delay:
                self.set1.update(self.set2)

        except IOError, e:
            if op.debug: print 'dstat_innodb_buffer: lost pipe to mysql,', e
            for name in self.vars: self.val[name] = -1

        except Exception, e:
            if op.debug: print 'dstat_innodb_buffer: exception', e
            for name in self.vars: self.val[name] = -1

# vim:ts=4:sw=4:et

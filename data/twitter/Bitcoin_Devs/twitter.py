import subprocess

since = '2017-01-01'
until = '2018-03-06'
for handle in open('handle_list.txt'):
    subprocess.call(['python', 'Exporter.py', \
                    '--username', handle[:-1], \
                    '--since', since, \
                    '--until', until, \
                    '--output', 'Bitcoin devs\\'+handle[:-1]+".csv" \
                   ])
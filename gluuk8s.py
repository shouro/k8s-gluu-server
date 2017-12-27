from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import click

STAGE2_TMPL = 'templates/stage2.yaml.tmpl'

def render_stage2(ctx):
    with open(STAGE2_TMPL, 'r') as fp:
      stage2_tmpl = fp.read()
    
    stage2 = stage2_tmpl.format(**ctx)

    print(stage2)


@click.command()
@click.option("--ldap-location",
              default="127.0.0.1:1389",
              help="Location for ldap server, Ex: <ip_or_name>:<port>",
              show_default=True)
@click.option("--k8s-gluu-hostname",
              default="k8s-gluu-hostname",
              help="Hostname for Gluu Server.",
              show_default=True)
def main(ldap_location, k8s_gluu_hostname):
  #validate ldap location
  if len(ldap_location.split(':')) != 2:
    print('invalid ldap location format')
    return

  for part in ldap_location.split(':'):
    if part == '':
      print('ldap url ({}) validation failed'.format(ldap_location))
      return

  ldap_ip = ldap_location.split(':')[0]
  
  try:
    ldap_port = int(ldap_location.split(':')[1])
  except ValueError:
    print('ldap port ({}) validation failed, not an integer'.format(ldap_location.split(':')[1]))
    return
  
  # render stage2.yaml
  ctx = {
    'k8s-gluu-hostname': k8s_gluu_hostname,
    'ldap_ip': ldap_ip,
    'ldap_port': ldap_port,
  }
  render_stage2(ctx)


if __name__ == "__main__":
    main()
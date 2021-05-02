import jinja2
import os

if __name__ == '__main__':
    access_file = "/configs/access_lists"
    nginx_keys_dir = "/etc/nginx/keys/live/"
    
    try:
        domain_dir = os.listdir(nginx_keys_dir)
        try:
            domain_dir.remove('README')
        except:
            pass
        domain = ''.join(domain_dir)
        ssl_certs_config = (
            f'ssl_certificate         keys/live/{domain}/cert.pem;\n' +
            f'        ssl_certificate_key     keys/live/{domain}/privkey.pem;'
        )
        template_file = "nginx.conf.template"
    except:
        template_file = "nginx-nossl.conf.template"

    with open(access_file) as f:
        acl_content = f.read().splitlines()
    
    acl_content = [ f"            allow {elem};" for elem in acl_content ]
  
    if len(acl_content) != 0:
        acl_content.append('            deny all;')

    acl_template = '\n'.join(acl_content)
    
    
    templateLoader = jinja2.FileSystemLoader(searchpath="/configs/")
    templateEnv = jinja2.Environment(loader = templateLoader)
    template = templateEnv.get_template(template_file)
    if template_file == "nginx.conf.template":
        outputText = template.render(ssl_certs = ssl_certs_config, access_list = acl_template)
    else: 
        outputText = template.render()
    
    print(outputText)

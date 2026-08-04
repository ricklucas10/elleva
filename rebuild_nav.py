import os

# Clean source files are in /Users/elon/Downloads/
sources = {
    'lamina1': '/Users/elon/Downloads/lamina_mazin_v5.html',
    'lamina2': '/Users/elon/Downloads/lamina_2_problema.html',
    'lamina3': '/Users/elon/Downloads/lamina_3_solucao.html',
    'lamina4': '/Users/elon/Downloads/lamina_4_lastro.html',
    'lamina5': '/Users/elon/Downloads/lamina_5_oportunidade.html',
    'lamina6': '/Users/elon/Downloads/lamina_6_rede.html',
}

nav_order = {
    'lamina1': ('deck.html', 'lamina2.html'),
    'lamina2': ('lamina1.html', 'lamina3.html'),
    'lamina3': ('lamina2.html', 'lamina4.html'),
    'lamina4': ('lamina3.html', 'lamina5.html'),
    'lamina5': ('lamina4.html', 'lamina6.html'),
    'lamina6': ('lamina5.html', 'deck.html'),
}

base_dir = '/Users/elon/elleva-deck'

NAV_CSS = """
  
  /* === NAVEGACAO === */
  body { position: relative; }
  .nav-arrow {
    position: fixed;
    top: 50%;
    transform: translateY(-50%);
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #c9a96e;
    font-size: 28px;
    text-decoration: none;
    border-radius: 3px;
    transition: all 0.3s;
    z-index: 100;
    cursor: pointer;
    background: rgba(8, 8, 14, 0.85);
    border: 1px solid rgba(200, 165, 100, 0.3);
    box-shadow: 0 0 12px rgba(0, 0, 0, 0.5);
  }
  .nav-arrow:hover {
    color: #fff;
    background: rgba(200, 165, 100, 0.15);
    border-color: rgba(200, 165, 100, 0.5);
    box-shadow: 0 0 20px rgba(200, 165, 100, 0.15);
  }
  .nav-prev { left: 24px; }
  .nav-next { right: 24px; }
"""

for name, source_path in sources.items():
    filename = f'{name}.html'
    prev, next_ = nav_order[name]
    
    with open(source_path) as f:
        html = f.read()
    
    # Inject nav CSS
    html = html.replace('</style>', NAV_CSS + '\n</style>')
    
    # Inject nav arrows right after <body>
    arrows = f'\n  <a class="nav-arrow nav-prev" href="{prev}">&#8592;</a>\n  <a class="nav-arrow nav-next" href="{next_}">&#8594;</a>\n'
    html = html.replace('<body>', '<body>' + arrows)
    
    # Fix image path for lamina1 (use base64 inline)
    if name == 'lamina1':
        img_path = '/Users/elon/Downloads/mazin_foto_oficial.png'
        if img_path in html:
            import base64
            with open(img_path, 'rb') as f:
                b64 = base64.b64encode(f.read()).decode()
            html = html.replace(img_path, 'data:image/png;base64,' + b64)
    
    out_path = os.path.join(base_dir, filename)
    with open(out_path, 'w') as f:
        f.write(html)
    
    # Verify
    ok = 'nav-arrow' in html and 'nav-prev' in html and 'nav-next' in html
    print(f'{"OK" if ok else "FALHA"} {filename}')

print('Pronto!')

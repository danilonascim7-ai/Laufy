# 1. Adicionado o 'jsonify' nos imports
from flask import Flask, request, render_template, redirect, jsonify

app = Flask(__name__)

# Seu "Banco de Dados" de peças. 
banco_produtos = [
    # ==================== PROCESSADORES (CPUs) ====================
    {"nome": "Kit X99 (Xeon E5 2680 V4 + Placa-mãe)", "tipo": "cpu", "marca": "intel", "preco": 350, "integrada": False},
    {"nome": "Ryzen 5 4600G + Placa-mãe A520M", "tipo": "cpu", "marca": "amd", "preco": 1000, "integrada": True},
    {"nome": "Ryzen 5 5500 + Placa-mãe A520M", "tipo": "cpu", "marca": "amd", "preco": 950, "integrada": False},
    {"nome": "Intel Core i3-12100F + Placa-mãe H610M", "tipo": "cpu", "marca": "intel", "preco": 980, "integrada": False},
    
    {"nome": "Ryzen 5 5600 + Placa-mãe B550M", "tipo": "cpu", "marca": "amd", "preco": 1300, "integrada": False},
    {"nome": "Intel Core i5-12400F + Placa-mãe H610M", "tipo": "cpu", "marca": "intel", "preco": 1350, "integrada": False},
    {"nome": "Ryzen 5 7600 + Placa-mãe B650M (DDR5)", "tipo": "cpu", "marca": "amd", "preco": 2200, "integrada": True},
    {"nome": "Intel Core i5-14600K + Placa-mãe B760M", "tipo": "cpu", "marca": "intel", "preco": 2600, "integrada": False},
    
    {"nome": "Ryzen 7 7800X3D + Placa-mãe B650M Premium", "tipo": "cpu", "marca": "amd", "preco": 3800, "integrada": True},
    {"nome": "Ryzen 9 7950X3D + Placa-mãe X670E", "tipo": "cpu", "marca": "amd", "preco": 5500, "integrada": True},
    {"nome": "Intel Core i9-14900K + Placa-mãe Z790", "tipo": "cpu", "marca": "intel", "preco": 5200, "integrada": False},

    # ==================== PLACAS DE VÍDEO (GPUs) ====================
    {"nome": "AMD Radeon RX 580 8GB", "tipo": "gpu", "marca": "amd", "preco": 600, "dedicada": True},
    {"nome": "NVIDIA GTX 1650 4GB", "tipo": "gpu", "marca": "nvidia", "preco": 680, "dedicada": True},
    {"nome": "AMD Radeon RX 6600 8GB", "tipo": "gpu", "marca": "amd", "preco": 1200, "dedicada": True},
    {"nome": "NVIDIA RTX 3050 6GB", "tipo": "gpu", "marca": "nvidia", "preco": 1150, "dedicada": True},
    {"nome": "NVIDIA RTX 4060 8GB", "tipo": "gpu", "marca": "nvidia", "preco": 1900, "dedicada": True},
    
    {"nome": "AMD Radeon RX 7700 XT 12GB", "tipo": "gpu", "marca": "amd", "preco": 2900, "dedicada": True},
    {"nome": "NVIDIA RTX 4070 Super 12GB", "tipo": "gpu", "marca": "nvidia", "preco": 4200, "dedicada": True},
    
    {"nome": "NVIDIA RTX 4080 Super 16GB", "tipo": "gpu", "marca": "nvidia", "preco": 7300, "dedicada": True},
    {"nome": "AMD Radeon RX 7900 XTX 24GB", "tipo": "gpu", "marca": "amd", "preco": 6900, "dedicada": True},
    {"nome": "NVIDIA RTX 4090 24GB (A Rainha)", "tipo": "gpu", "marca": "nvidia", "preco": 12500, "dedicada": True},
    {"nome": "NVIDIA RTX 5070 12GB", "tipo": "gpu", "marca": "nvidia", "preco": 6850, "dedicada": True},

    
    
    
    # ==================== PEÇAS BASE OBRIGATÓRIAS ====================
    {"nome": "Kit Base Econômico (16GB RAM DDR4 + SSD 512GB + Fonte 500W + Gabinete)", "tipo": "base_baixo", "preco": 520},
    {"nome": "Kit Base Premium (32GB RAM DDR5 + SSD NVMe 2TB + Fonte 850W Gold + Water Cooler + Gabinete Gamer)", "tipo": "base_alto", "preco": 1600}
]

# 2. A Função de Filtro modificada para retornar um Dicionário em vez de texto cru
def filtrar_melhor_setup(orcamento_min, orcamento_max, preferencia, tipopl, foco, produtos):
    if orcamento_max <= 4000:
        pecas_base = [p for p in produtos if p["tipo"] == "base_baixo"]
    else:
        pecas_base = [p for p in produtos if p["tipo"] == "base_alto"]
        
    custo_base = sum(p["preco"] for p in pecas_base)
    nome_base = pecas_base[0]["nome"] if pecas_base else "Componentes básicos"

    cpus = [p for p in produtos if p["tipo"] == "cpu"]
    if preferencia != "custo":
        cpus = [c for c in cpus if c["marca"] == preferencia]
    if tipopl == "integrada":
        cpus = [c for c in cpus if c["integrada"] is True]

    gpus = [p for p in produtos if p["tipo"] == "gpu"]
    if tipopl == "integrada":
        gpus = []
    elif tipopl == "dedicada":
        gpus = [g for g in gpus if g["dedicada"] is True]

    deve_inverter = True if foco == "desempenho" else False
    cpus.sort(key=lambda x: x["preco"], reverse=deve_inverter)
    gpus.sort(key=lambda x: x["preco"], reverse=deve_inverter)

    # Agora retornamos um dicionário estruturado para facilitar o trabalho do JavaScript
    for cpu in cpus:
        if tipopl == "integrada":
            preco_total = custo_base + cpu["preco"]
            if orcamento_min <= preco_total <= orcamento_max:
                return {
                    "sucesso": True,
                    "cpu": cpu['nome'],
                    "gpu": "Vídeo Integrado",
                    "base": nome_base,
                    "preco": preco_total
                }
        else:
            for gpu in gpus:
                preco_total = custo_base + cpu["preco"] + gpu["preco"]
                if orcamento_min <= preco_total <= orcamento_max:
                    return {
                        "sucesso": True,
                        "cpu": cpu['nome'],
                        "gpu": gpu['nome'],
                        "base": nome_base,
                        "preco": preco_total
                    }

    return {"sucesso": False, "mensagem": "Nenhuma configuração ideal foi encontrada para este orçamento com os filtros selecionados."}

@app.route("/")
def home():
    return render_template("index.html")

# 3. Rota de Resultados alterada para retornar JSONIFY
@app.route("/resultado", methods=["POST"])
def resultado():
    orcamento_selecionado = request.form["orcamento"]
    preferencia = request.form["preferencia"].lower()
    tipopl = request.form["tipopl"].lower()
    foco = request.form["foco"].lower()

    limites_orcamento = {
        "1015": (1000, 1500),
        "1520": (1500, 2000),
        "2025": (2000, 2500),
        "2530": (2500, 3000),
        "3035": (3000, 3500),
        "3540": (3500, 4000),
        "4045": (4000, 4500),
        "4550": (4500, 5000),
        "5055": (5000, 5500),
        "5560": (5500, 6000),
        "6065": (6000, 6500),
        "6570": (6500, 7000),
        "7075": (7000, 7500),
        "7580": (7500, 8000),
        "8085": (8000, 8500),
        "8590": (8500, 9000),
        "9095": (9000, 9500),
        "95100": (9500, 10000),
        "100110": (10000, 11000),
        "110120": (11000, 12000),
        "120130": (12000, 13000),
        "130140": (13000, 14000),
        "140150": (14000, 15000)
    
    }
    
    orc_min, orc_max = limites_orcamento.get(orcamento_selecionado, (1000, 1500))

    config_gerada = filtrar_melhor_setup(orc_min, orc_max, preferencia, tipopl, foco, banco_produtos)

    # Em vez de render_template, agora mandamos os dados puros em JSON!
    return jsonify(config_gerada)

@app.route('/Twitch')
def discord():
    return redirect("https://www.twitch.tv/danihn") 

@app.route('/ads.txt')
def ads_txt():
    return app.send_static_file('ads.txt')

@app.route('/git')
def github():
    return redirect('https://github.com/danilonascim7-ai')

@app.route('/home')
def homes():
    return render_template('index.html')

@app.route('/nos')
def retur():
    return render_template('index2.html')

@app.route('/Pol')
def pole():
    return render_template('index3.html')

@app.route('/insta')
def inst():
    return redirect('https://www.instagram.com/laufyoficial/')

@app.route('/x')
def x():
    return redirect('https://x.com/laufyoficial')

if __name__ == "__main__":
    app.run(debug=True)
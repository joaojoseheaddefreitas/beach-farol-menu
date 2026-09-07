#!/usr/bin/env python3
"""Gera o DEFAULT_CATEGORIAS do Beach Farol (cardapio fisico) em public/app/index.html.
Textos/fotos aproveitados do index_62 original (Cook Control) onde o item coincide;
fotos novas do ZIP via CDN; item sem foto boa fica com images/sem-foto.svg."""
import json, os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'public/app/index.html')
U = {}
for f in glob.glob(os.path.join(ROOT, 'src/assets/*.asset.json')):
    U[os.path.basename(f).replace('.asset.json', '')] = json.load(open(f))['url']

NOIMG = 'images/sem-foto.svg'
BALDE = 'images/balde-cerveja.jpg'
def A(k): return U[k]

# ---- fotos externas do index_62 original (todas testadas, HTTP 200) ----
O = {
 'passarinho': 'https://images.unsplash.com/photo-1626645738196-c2a7c87a8f58?w=600&q=80',
 'isca_frango': 'https://images.unsplash.com/photo-1562967914-608f82629710?w=600&q=80',
 'isca_frango_completa': 'https://images.pexels.com/photos/36879227/pexels-photo-36879227.jpeg',
 'isca_peixe_completa': 'https://images.pexels.com/photos/37492315/pexels-photo-37492315.jpeg',
 'polvo_camarao': 'https://images.unsplash.com/photo-1625944230945-1b7dd3b949ab?w=600&q=80',
 'polvo': 'https://images.pexels.com/photos/17243887/pexels-photo-17243887.jpeg',
 'caldo': 'https://images.unsplash.com/photo-1547592180-85f173990554?w=600&q=80',
 'bacalhau': 'https://media.istockphoto.com/id/1061650994/pt/foto/cod-cake.jpg?b=1&s=612x612&w=0&k=20&c=',
 'bolinho_peixe': 'https://images.pexels.com/photos/35001790/pexels-photo-35001790.jpeg',
 'arrumadinho': 'https://images.pexels.com/photos/37017289/pexels-photo-37017289.jpeg',
 'escondidinho': 'https://media.istockphoto.com/id/1316618702/pt/foto/pastel-de-choclo-chilean-beef-and-corn',
 'moqueca_peixe': 'https://media.istockphoto.com/id/1252504256/pt/foto/brazilian-cuisine-shrimp-stew-usually-',
 'moqueca_mista': 'https://media.istockphoto.com/id/1298662915/pt/foto/typical-dish-of-brazilian-cuisine-call',
 'peixe_frito_g': 'https://media.istockphoto.com/id/1365037894/pt/foto/food-fish.jpg?s=1024x1024&w=is&k=20&c=',
 'mariscada': 'https://images.pexels.com/photos/33597325/pexels-photo-33597325.jpeg',
 'arroz': 'https://images.pexels.com/photos/17563535/pexels-photo-17563535.jpeg',
 'feijao': 'https://images.pexels.com/photos/19870149/pexels-photo-19870149.jpeg',
 'farofa': 'https://media.istockphoto.com/id/1304992289/pt/foto/bacon-crumbs-with-dried-meat-a-very-po',
 'vinagrete': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600&q=80',
 'pirao': 'https://images.pexels.com/photos/9200399/pexels-photo-9200399.jpeg',
 'maracuja': 'https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=600&q=80',
 'refri_lata': 'https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=600&q=80',
 'agua': 'https://images.pexels.com/photos/35020123/pexels-photo-35020123.jpeg',
 'energetico': 'https://images.pexels.com/photos/17220086/pexels-photo-17220086.jpeg',
 'cachaca': 'https://images.pexels.com/photos/7601301/pexels-photo-7601301.jpeg',
 'whisky_dose': 'https://media.istockphoto.com/id/521210078/pt/foto/copo-de-u%C3%ADsque-escoc%C3%',
 'heineken_600': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSAEkZ7oNhy7kuoS6pY0paDmb7P',
 'caipirinha': 'https://images.pexels.com/photos/29863905/pexels-photo-29863905.jpeg',
}
# Recupera URLs completas das fotos originais (as chaves acima sao prefixos)
_orig = json.load(open(os.path.join(ROOT, '.lovable/orig_items.json'))) if os.path.exists(os.path.join(ROOT, '.lovable/orig_items.json')) else []
for k, v in list(O.items()):
    for it in _orig:
        if it['img'].startswith(v): O[k] = it['img']; break

ACOMP_MOQ = 'Acompanha arroz, pirão, feijão fradinho e farofa.'
ACOMP_FRITO = 'Acompanha arroz, vinagrete, feijão fradinho, farofa e batata frita.'
ACOMP_EXEC = 'Acompanha arroz, legumes e purê de batata.'
QUENTE = 'Combo Bebidas Quentes: garrafa + 2 Red Bull + 2 gelos de coco.'

CATS = []
def cat(id, nome, icone): CATS.append(dict(id=id, nome=nome, icone=icone, itens=[])); return CATS[-1]
def it(c, id, nome, preco, desc, porcao, tempo, sub, img=NOIMG, novo=False):
    c['itens'].append(dict(id=id, nome=nome, preco=preco, desc=desc, porcao=porcao, tempo=tempo, sub=sub, ativo=True, novo=novo, img=img))

# ═════════════ PETISCOS ═════════════
c = cat('petiscos', 'Petiscos & Entradas', '🦐'); S = 'Petiscos (300g)'
it(c,'pet_batata_frita','Batata Frita',30,'Batatas fritas crocantes salpicadas com orégano e sal marinho.','300g',15,S,A('orig-batata-frita.jpg'))
it(c,'pet_carne_sol_fritas','Carne do Sol c/ Fritas',75,'Batata frita palito crocante + carne do sol na manteiga de garrafa. O clássico da praia!','300g',25,S,A('orig-carne-sol-fritas.jpg'))
it(c,'pet_carne_sol_farofa','Carne do Sol com Farofa e Salada',75,'Carne do sol acebolada na manteiga de garrafa, acompanhada de farofa e salada.','300g',25,S,A('orig-carne-sol-aipim.jpg'))
it(c,'pet_nordestao','Nordestão',85,'Carne do sol, calabresa, queijo coalho, farofa, macaxeira frita e salada.','300g',25,S)
it(c,'pet_arrumadinho','Arrumadinho',85,'Carne do sol, feijão verde, farofa e vinagrete.','300g',25,S,O['arrumadinho'])
it(c,'pet_barca_mista','Barca Mista',205,'Camarão, isca de peixe, lula, carne do sol, calabresa, batata frita e salada. Para compartilhar.','Serve 3-4',35,S)
it(c,'pet_camarao_alho','Camarão ao Alho e Óleo',65,'Camarão salteado no azeite com muito alho e cheiro-verde.','300g',15,S,A('orig-camarao-alho-oleo.jpg'))
it(c,'pet_camarao_milanesa','Camarão à Milanesa',90,'Camarões grandes empanados e fritos, crocantes por fora. Com molho tartar.','300g',18,S,A('orig-camarao-milanesa.jpg'))
it(c,'pet_camarao_coalho','Camarão c/ Queijo Coalho na Chapa',90,'Camarão grelhado na chapa com cubos de queijo coalho dourado.','300g',18,S)
it(c,'pet_queijo_coalho','Queijo Coalho na Chapa',30,'Queijo coalho dourado na chapa, servido com melaço.','300g',10,S)
it(c,'pet_lambreta','Lambreta',50,'Lambreta cozida no vapor com tomate, cebola e coentro. Acompanha copo de caldo quente.','Dúzia + caldo',15,S,A('orig-lambreta.jpg'))
it(c,'pet_caranguejo','Caranguejo com Pirão (3 unid.)',55,'Caranguejos cozidos no bafo com tempero verde fresco e leite de coco. Acompanha pirão e vinagrete.','3 unidades',20,S,A('orig-caranguejo.jpg'))
it(c,'pet_acaraje_unid','Acarajé Completo (unid.)',25,'Acarajé tradicional com vatapá, caruru, camarão seco e salada.','1 unidade',10,S)
it(c,'pet_acaraje_10','Acarajé Porção 10 unid.',45,'Porção de mini acarajés com vatapá e camarão. Ideal para compartilhar.','10 unidades',15,S)
it(c,'pet_passarinha','Porção de Passarinha',35,'Passarinha (baço) acebolada e bem temperada. Acompanha farofa e salada.','300g',20,S)
it(c,'pet_frango_passarinho','Frango à Passarinho',65,'Frango à passarinho crocante, tempero da casa. Acompanha farofa e salada.','300g',20,S,O['passarinho'])
it(c,'pet_isca_frango','Isca de Frango',65,'Iscas de frango fritas, douradas e crocantes. Acompanha farofa e salada.','300g',20,S,O['isca_frango'])
it(c,'pet_isca_peixe','Isca de Peixe',85,'Iscas de peixe douradas e sequinhas. Acompanha farofa e salada.','300g',20,S)
it(c,'pet_isca_frango_completa','Isca Completa de Frango',85,'Iscas de frango fritas com farofa, salada e batata frita.','Serve 2',20,S,O['isca_frango_completa'])
it(c,'pet_isca_peixe_completa','Isca Completa de Peixe',105,'Iscas de peixe douradas com farofa, salada e batata frita.','Serve 2',20,S,O['isca_peixe_completa'])
it(c,'pet_pititinga','Pititinga',55,'Peixinhos locais inteiros empanados e fritos bem sequinhos. Acompanha farofa e salada.','300g',20,S,A('orig-pititinga.jpg'))
it(c,'pet_mix_pasteis','Mix de Pastéis – Cesta 6 unid.',40,'Cesta com 6 pastéis: sabores carne, camarão e queijo.','6 unidades',15,S)
S = 'Bolinhos (8 unid.)'
it(c,'bol_camarao_encapotado','Camarão Encapotado',45,'Camarões inteiros envoltos em massa crocante. Acompanha molho da casa.','8 unidades',15,S)
it(c,'bol_misto','Bolinho Misto',35,'Bolinhos sortidos fritos, crocantes por fora e cremosos por dentro.','8 unidades',15,S,O['bolinho_peixe'])
it(c,'bol_bacalhau','Bolinho de Bacalhau',40,'Bolinhos crocantes por fora e cremosos por dentro. Receita portuguesa.','8 unidades',15,S,O['bacalhau'])
it(c,'bol_charque','Bolinho de Charque',40,'Bolinho de charque desfiado com massa de aipim. Crocante e bem temperado.','8 unidades',15,S)
it(c,'bol_coxinha','Coxinha de Frango c/ Requeijão',40,'Coxinhas de frango cremosas com requeijão.','8 unidades',15,S)
S = 'Caldos'
it(c,'cal_sururu','Caldo de Sururu',30,'Caldo de sururu cremoso com leite de coco e coentro. Ideal para esquentar.','300 ml',10,S,O['caldo'])
it(c,'cal_camarao','Caldo de Camarão',30,'Caldo reforçado de camarão com pimenta a gosto.','300 ml',10,S,O['caldo'])
it(c,'cal_polvo','Caldo de Polvo',30,'Caldo de polvo encorpado, temperado com cheiro-verde.','300 ml',10,S,O['caldo'])

# ═════════════ PRATOS ═════════════
c = cat('pratos', 'Pratos', '🍽️'); S = 'Pratos Executivos'
it(c,'exe_bife_cavalo','Bife à Cavalo',50,'Bife grelhado com ovo, arroz, feijão, vinagrete e batata frita.','Individual',25,S,A('bife-a-cavalo.jpg'))
it(c,'exe_file_carne_parm','Filé de Carne à Parmegiana',60,'Filé bovino empanado ao molho de tomate e queijo gratinado. '+ACOMP_EXEC,'Individual',30,S,A('file-carne-parmegiana.jpg'))
it(c,'exe_frango_grelhado','Filé de Frango Grelhado',60,'Filé de frango grelhado no ponto. '+ACOMP_EXEC,'Individual',25,S)
it(c,'exe_frango_parm','Filé de Frango à Parmegiana',60,'Filé de frango empanado ao molho de tomate e queijo gratinado. '+ACOMP_EXEC,'Individual',30,S,A('parmegiana-de-frango.jpg'))
it(c,'exe_posta_grelhada','Posta de Peixe Grelhada',50,'Posta de peixe grelhada, no ponto. '+ACOMP_EXEC,'Individual',25,S,A('posta-de-peixe-grelhada.jpg'))
it(c,'exe_strog_frango','Strogonoff de Frango',50,'Strogonoff de frango cremoso. Acompanha arroz e batata palha.','Individual',25,S,A('strogonoff-de-frango.jpg'))
it(c,'exe_strog_camarao','Strogonoff de Camarão',65,'Strogonoff de camarão cremoso. Acompanha arroz e batata palha.','Individual',25,S,A('strogonoff-de-camarao.jpg'))
S = 'Pratos Especiais'
it(c,'esp_escond_frango','Escondidinho de Frango',100,'Frango desfiado com purê de aipim cremoso, gratinado. Acompanha arroz e vinagrete.','Serve 2',30,S)
it(c,'esp_escond_carne_sol','Escondidinho de Carne do Sol',110,'Carne do sol desfiada com purê de aipim cremoso, gratinado. Acompanha arroz e vinagrete.','Serve 2',30,S,O['escondidinho'])
it(c,'esp_escond_camarao','Escondidinho de Camarão',120,'Camarão ao molho com purê de aipim cremoso, gratinado. Acompanha arroz e vinagrete.','Serve 2',30,S)
it(c,'esp_carne_sol_sertaneja','Carne do Sol Sertaneja',150,'Carne do sol na manteiga de garrafa com macaxeira, queijo coalho, farofa e vinagrete.','Serve 2-3',35,S)
it(c,'esp_picanha_chapa','Picanha na Chapa',170,'Picanha fatiada na chapa. Acompanha arroz, feijão tropeiro, vinagrete e batata frita.','Serve 2-3',35,S)
it(c,'esp_picanha_suina','Picanha Suína',120,'Picanha suína na chapa. Acompanha arroz, feijão fradinho, farofa e vinagrete.','Serve 2',35,S)
it(c,'esp_salmao_camarao','Salmão na Chapa com Camarão',170,'Salmão grelhado coberto com camarões. Acompanha arroz, legumes e purê de batata.','Serve 2',35,S)
it(c,'esp_fettuccine','Fettuccine de Camarão',100,'Fettuccine ao molho cremoso com camarões e parmesão.','Serve 2',30,S)
it(c,'esp_abacaxi_tropical','Abacaxi Tropical',120,'Abacaxi recheado com camarão cremoso e queijo gratinado.','Serve 2',35,S)
it(c,'esp_salada_polvo','Salada de Polvo',150,'Polvo cozido no ponto, ao vinagrete fresco com legumes.','Serve 2',25,S,O['polvo'])
it(c,'esp_salada_polvo_camarao','Salada de Polvo com Camarão',180,'Polvo e camarão ao vinagrete fresco. Acompanha legumes, arroz, farofa e purê de batata.','Serve 2-3',25,S,O['polvo_camarao'])
it(c,'esp_chapa_prime','Chapa Prime',200,'Polvo grelhado, anéis de lula, camarão e lagosta grelhada – 200g cada.','Serve 3-4',40,S)
S = 'Moquecas & Peixes Fritos'
it(c,'moq_vermelho','Moqueca de Vermelho',200,'Vermelho fresco no leite de coco, azeite de dendê e coentro. '+ACOMP_MOQ,'Serve 2-3',40,S,O['moqueca_peixe'])
it(c,'moq_corvina','Moqueca de Corvina',170,'Corvina no leite de coco, azeite de dendê e coentro. '+ACOMP_MOQ,'Serve 2-3',40,S,O['moqueca_mista'])
it(c,'moq_pescada','Moqueca de Pescada Amarela',220,'Pescada amarela no leite de coco, azeite de dendê e coentro. '+ACOMP_MOQ,'Serve 2-3',40,S)
it(c,'moq_camarao','Moqueca de Camarão',200,'Camarões frescos no leite de coco caseiro, azeite de dendê e coentro. '+ACOMP_MOQ,'Serve 2-3',40,S,A('orig-moqueca-camarao.jpg'))
it(c,'moq_mista','Moqueca Mista',250,'Peixe e camarão no leite de coco, azeite de dendê e coentro. '+ACOMP_MOQ,'Serve 3-4',40,S)
it(c,'moq_mariscada','Mariscada',270,'Seleção completa de frutos do mar: camarão, polvo, peixe e lagosta. '+ACOMP_MOQ,'Serve 3-4',45,S,O['mariscada'])
it(c,'pf_corvina','Corvina Frita Inteira',170,'Corvina inteira frita na hora. '+ACOMP_FRITO,'Serve 2-3',35,S,O['peixe_frito_g'])
it(c,'pf_vermelho','Peixe Vermelho Frito Inteiro',200,'Peixe vermelho do dia frito inteiro na hora. '+ACOMP_FRITO,'Serve 2-3',35,S,A('orig-peixe-frito-inteiro.jpg'))
it(c,'pf_pescada_posta','Pescada Amarela Frita em Posta',160,'Postas de pescada amarela fritas e sequinhas. Acompanha arroz, vinagrete, feijão fradinho e farofa.','Serve 2',30,S,A('posta-de-peixe-frita.jpg'))
S = 'Guarnições'
it(c,'gua_arroz','Arroz',10,'Arroz branco soltinho preparado com alho e azeite.','300g',5,S,O['arroz'])
it(c,'gua_feijao_fradinho','Feijão Fradinho',15,'Feijão fradinho temperado, porção extra.','300g',5,S,O['feijao'])
it(c,'gua_feijao_tropeiro','Feijão Tropeiro',20,'Feijão tropeiro com farinha, bacon e calabresa.','300g',5,S)
it(c,'gua_vinagrete','Vinagrete',10,'Tomate, pimentão, cebola, coentro e azeite. Bem temperado.','200g',5,S,O['vinagrete'])
it(c,'gua_farofa','Farofa',10,'Farofa crocante temperada com manteiga de garrafa.','300g',5,S,O['farofa'])
it(c,'gua_pirao','Pirão de Moqueca',20,'Pirão cremoso feito com o caldo da moqueca.','300g',5,S,O['pirao'])

# ═════════════ BEBIDAS ═════════════
c = cat('bebidas', 'Bebidas', '🍹'); S = 'Cervejas 600ml'
it(c,'cerv_itaipava_600','Itaipava 600ml',14,'Cerveja Itaipava gelada, garrafa de 600ml para compartilhar.','600 ml',5,S,A('orig-itaipava-600.jpg'))
it(c,'cerv_amstel_600','Amstel 600ml',18,'Cerveja Amstel gelada, garrafa 600ml.','600 ml',5,S)
it(c,'cerv_stella_600','Stella Artois 600ml',22,'Cerveja Stella Artois gelada, garrafa 600ml.','600 ml',5,S,A('orig-stella-600.jpg'))
it(c,'cerv_heineken_600','Heineken 600ml',22,'Cerveja Heineken gelada, garrafa 600ml.','600 ml',5,S,O['heineken_600'])
it(c,'cerv_imperio_600','Império Lager 600ml',18,'Cerveja Império Lager gelada, garrafa 600ml.','600 ml',5,S)
it(c,'cerv_original_600','Antarctica Original 600ml',22,'Cerveja Antarctica Original gelada, garrafa 600ml.','600 ml',5,S)
S = 'Long Necks'
it(c,'ln_imperio_ultra','Império Ultra',14,'Long neck Império Ultra gelada.','Long neck',5,S)
it(c,'ln_imperio_lager','Império Lager Long Neck',13,'Long neck Império Lager gelada.','Long neck',5,S,BALDE)
it(c,'ln_budweiser','Budweiser Long Neck',15,'Long neck Budweiser gelada.','Long neck',5,S,BALDE)
it(c,'ln_heineken','Heineken Long Neck',17,'Long neck Heineken gelada.','Long neck',5,S,A('longneck-heineken-balde.jpg'))
it(c,'ln_heineken_zero','Heineken s/ Álcool',17,'Long neck Heineken 0.0 gelada.','Long neck',5,S)
it(c,'ln_corona','Corona Long Neck',18,'Long neck Corona gelada, com limão.','Long neck',5,S,BALDE)
it(c,'ln_corona_zero','Corona s/ Álcool',18,'Long neck Corona Cero gelada.','Long neck',5,S,A('longneck-corona-zero.webp'))
it(c,'ln_coronita','Coronita 210ml',14,'Coronita gelada, 210ml.','210 ml',5,S)
it(c,'ln_stella_gold','Stella Gold s/ Glúten',17,'Long neck Stella Artois Gold sem glúten gelada.','Long neck',5,S,A('longneck-stella-sem-gluten.jpg'))
it(c,'ln_malzbier','Malzbier Lata ou Long Neck',16,'Malzbier gelada, lata ou long neck.','Unidade',5,S)
it(c,'ln_ice_smirnoff','Ice Smirnoff',18,'Smirnoff Ice gelada.','Long neck',5,S,BALDE)
it(c,'ln_ice_51','Ice 51',16,'51 Ice gelada.','Long neck',5,S,BALDE)
it(c,'ln_ice_leev','Ice Leev',12,'Ice Leev gelada.','Long neck',5,S)
S = 'Combos – 5 Cervejas 600ml'
it(c,'combo600_itaipava','Combo 5 Itaipava 600ml',53,'Balde com 5 garrafas Itaipava 600ml geladas.','5 un · 600 ml',5,S,A('combo-itaipava-600.jpg'))
it(c,'combo600_amstel','Combo 5 Amstel 600ml',77,'Balde com 5 garrafas Amstel 600ml geladas.','5 un · 600 ml',5,S,BALDE)
it(c,'combo600_stella','Combo 5 Stella Artois 600ml',93,'Balde com 5 garrafas Stella Artois 600ml geladas.','5 un · 600 ml',5,S,BALDE)
it(c,'combo600_heineken','Combo 5 Heineken 600ml',93,'Balde com 5 garrafas Heineken 600ml geladas.','5 un · 600 ml',5,S,A('combo-heineken-600.jpg'))
it(c,'combo600_imperio','Combo 5 Império Lager 600ml',76,'Balde com 5 garrafas Império Lager 600ml geladas.','5 un · 600 ml',5,S,BALDE)
it(c,'combo600_original','Combo 5 Antarctica Original 600ml',93,'Balde com 5 garrafas Antarctica Original 600ml geladas.','5 un · 600 ml',5,S,BALDE)
S = 'Combos – 5 Long Necks'
it(c,'comboln_budweiser','Combo 5 Budweiser',60,'Balde com 5 long necks Budweiser geladas.','5 long necks',5,S,BALDE)
it(c,'comboln_corona','Combo 5 Corona',78,'Balde com 5 long necks Corona geladas.','5 long necks',5,S,BALDE)
it(c,'comboln_heineken','Combo 5 Heineken',73,'Balde com 5 long necks Heineken geladas.','5 long necks',5,S,A('combo-longneck-heineken.jpg'))
it(c,'comboln_heineken_zero','Combo 5 Heineken s/ Álcool',73,'Balde com 5 long necks Heineken 0.0 geladas.','5 long necks',5,S,A('combo-heineken-prata.jpg'))
it(c,'comboln_coronita','Combo 5 Coronita',66,'Balde com 5 Coronitas geladas.','5 un · 210 ml',5,S,BALDE)
it(c,'comboln_corona_zero','Combo 5 Corona s/ Álcool',78,'Balde com 5 long necks Corona Cero geladas.','5 long necks',5,S,A('longneck-corona-zero.webp'))
it(c,'comboln_imperio_lager','Combo 5 Império Lager',53,'Balde com 5 long necks Império Lager geladas.','5 long necks',5,S,BALDE)
it(c,'comboln_imperio_ultra','Combo 5 Império Ultra',55,'Balde com 5 long necks Império Ultra geladas.','5 long necks',5,S,BALDE)
it(c,'comboln_stella_gluten','Combo 5 Stella s/ Glúten',84,'Balde com 5 long necks Stella Gold sem glúten geladas.','5 long necks',5,S,A('longneck-stella-sem-gluten.jpg'))
it(c,'comboln_smirnoff','Combo 5 Smirnoff Ice',77,'Balde com 5 unidades Smirnoff Ice geladas.','5 unidades',5,S,BALDE)
it(c,'comboln_51ice','Combo 5 51 Ice',78,'Balde com 5 unidades 51 Ice geladas.','5 unidades',5,S,BALDE)
it(c,'comboln_ice_leev','Combo 5 Ice Leev',45,'Balde com 5 long necks Ice Leev geladas.','5 long necks',5,S,BALDE)
S = 'Drinks'
it(c,'drk_mojito','Mojito',35,'Suco de limão, água com gás, rum e hortelã.','Taça 300 ml',8,S)
it(c,'drk_bob_marley','Bob Marley',35,'Licor de menta, groselha e suco de laranja.','Taça 300 ml',8,S)
it(c,'drk_aperol','Aperol Spritz',35,'Espumante, Aperol e soda.','Taça 300 ml',8,S)
it(c,'drk_gin_tonica','Gin Tônica',35,'Gin Tanqueray e água tônica.','Taça 300 ml',8,S)
it(c,'drk_sangria','Sangria',35,'Vinho tinto, frutas vermelhas, soda e suco de laranja.','Taça 300 ml',8,S)
it(c,'drk_sex_beach','Sex on the Beach',35,'Suco de laranja, licor de pêssego, granadina e vodka.','Taça 300 ml',8,S)
it(c,'drk_margarita','Margarita Frozen',35,'Tequila, gelo, Cointreau e suco de limão.','Taça 300 ml',8,S)
it(c,'drk_blue_lagoon','Blue Lagoon',35,'Suco de limão, vodka e curaçau blue.','Taça 300 ml',8,S)
it(c,'drk_moscow_mule','Moscow Mule',35,'Vodka Absolut, sumo de limão, xarope de gengibre e espuma de gengibre.','Caneca 300 ml',8,S)
it(c,'drk_beach_farol','Beach Farol Drink',35,'Vodka blue, licor de menta, sumo de limão e leite condensado. O drink da casa!','Taça 300 ml',8,S,novo=True)
it(c,'drk_chivas_colins','Chivas Colins',40,'Whisky Chivas 12 anos, xarope de gengibre, soda e sumo de limão.','Taça 300 ml',8,S)
it(c,'drk_43_sensacoes','43 Sensações',40,'Licor 43, vodka, sumo de limão e maracujá.','Taça 300 ml',8,S)
it(c,'drk_spicy_lemonade','Spicy Lemonade',40,'50ml Absolut Tabasco, 15ml suco de limão, 150ml Schweppes Citrus e 1 limão taiti ou siciliano.','Taça 300 ml',8,S)
it(c,'drk_bloody_mary','Blood Mary',40,'50ml Absolut Tabasco, 30ml suco de tomate, 10ml molho inglês, pitada de sal, pimenta do reino e 1 limão taiti.','Taça 300 ml',8,S)
it(c,'drk_magic_candy_sem','Magic Candy (s/ álcool)',35,'Morango, leite condensado, marshmallow, granulado e espuma especial.','Taça 300 ml',8,S)
it(c,'drk_magic_candy_com','Magic Candy (c/ álcool)',40,'Morango, leite condensado, marshmallow, granulado, espuma especial e vodka.','Taça 300 ml',8,S)
it(c,'drk_choc_sem','Choc Drink (s/ álcool)',30,'Leite condensado, creme de leite, cacau em pó e leite líquido.','Taça 300 ml',8,S)
it(c,'drk_choc_com','Choc Drink (c/ álcool)',35,'Leite condensado, creme de leite, cacau em pó, leite líquido e vodka.','Taça 300 ml',8,S)
it(c,'drk_coquetel_morango_sem','Coquetel de Morango (s/ álcool)',25,'Leite condensado, abacaxi, morango e gelo.','Taça 300 ml',8,S)
it(c,'drk_coquetel_morango_com','Coquetel de Morango (c/ álcool)',30,'Leite condensado, abacaxi, morango, gelo e vodka.','Taça 300 ml',8,S)
S = 'Caipirinha / Caipiroska'
it(c,'cai_caipirinha','Caipirinha',20,'Cachaça, limão taiti, açúcar e gelo. Consultar frutas disponíveis.','300 ml',8,S,O['caipirinha'])
it(c,'cai_caipirissima','Caipiríssima',30,'Rum, limão, açúcar e gelo. Consultar frutas disponíveis.','300 ml',8,S,A('caipiras-diversas.jpg'))
it(c,'cai_caipiroska_nac','Caipiroska de Fruta (vodka nacional)',25,'Vodka nacional, fruta da estação, açúcar e gelo. Consultar frutas disponíveis.','300 ml',8,S,A('caipiras-diversas.jpg'))
it(c,'cai_caipiroska_imp','Caipiroska de Fruta (vodka importada)',30,'Vodka importada, fruta da estação, açúcar e gelo. Consultar frutas disponíveis.','300 ml',8,S,A('caipiras-diversas.jpg'))
S = 'Sucos 500ml'
it(c,'suc_laranja','Suco de Laranja',18,'Suco natural de laranja feito na hora.','500 ml',5,S)
it(c,'suc_abacaxi','Suco de Abacaxi',18,'Suco natural de abacaxi batido na hora.','500 ml',5,S)
it(c,'suc_morango','Suco de Morango',20,'Suco natural de morango batido na hora.','500 ml',5,S)
it(c,'suc_limao','Suco de Limão',18,'Limonada natural gelada.','500 ml',5,S)
it(c,'suc_maracuja','Suco de Maracujá',18,'Suco natural de maracujá batido na hora. Consultar frutas disponíveis.','500 ml',5,S,O['maracuja'])
S = 'Diversos'
it(c,'div_refri_lata','Refrigerante Lata',7,'Coca-Cola, Guaraná Antarctica ou Sprite. Gelada.','350 ml',3,S,O['refri_lata'])
it(c,'div_h2o','H2OH!',8,'H2OH! gelada.','500 ml',3,S)
it(c,'div_coco_verde','Coco Verde',7,'Água de coco fresca direto do coqueiro, servida gelada na praia.','1 unidade',3,S,A('agua-de-coco.jpg'))
it(c,'div_coco_jarra','Coco na Jarra',15,'Jarra de água de coco gelada.','1 L',3,S)
it(c,'div_agua_sem_gas','Água s/ Gás',5,'Água mineral natural gelada.','500 ml',3,S,O['agua'])
it(c,'div_agua_com_gas','Água c/ Gás',6,'Água mineral com gás gelada.','500 ml',3,S,O['agua'])
it(c,'div_tonica','Água Tônica',7,'Água tônica gelada.','350 ml',3,S)
it(c,'div_red_bull','Energético Red Bull',16,'Energético Red Bull gelado.','250 ml',3,S,O['energetico'])
it(c,'div_sumo_limao','Sumo de Limão',2,'Sumo de limão espremido na hora.','Dose',3,S)
S = 'Doses'
it(c,'dos_licor43','Licor 43',30,'Dose de Licor 43.','50 ml',3,S)
it(c,'dos_gold_label','Whisky Gold Label',45,'Dose de Johnnie Walker Gold Label.','50 ml',3,S,O['whisky_dose'])
it(c,'dos_red_label','Whisky Red Label',25,'Dose de Johnnie Walker Red Label.','50 ml',3,S,O['whisky_dose'])
it(c,'dos_chivas','Whisky Chivas Regal',30,'Dose de Chivas Regal 12 anos.','50 ml',3,S,O['whisky_dose'])
it(c,'dos_old_parr','Whisky Old Parr',30,'Dose de Old Parr 12 anos.','50 ml',3,S,O['whisky_dose'])
it(c,'dos_buchanans','Buchanan\'s',35,'Dose de Buchanan\'s 12 anos.','50 ml',3,S,O['whisky_dose'])
it(c,'dos_conhaque_dreher','Conhaque Dreher',10,'Dose de conhaque Dreher.','50 ml',3,S)
it(c,'dos_conhaque_alcatrao','Conhaque Alcatrão',10,'Dose de conhaque de alcatrão.','50 ml',3,S)
it(c,'dos_conhaque_domecq','Conhaque Domecq',15,'Dose de conhaque Domecq.','50 ml',3,S)
it(c,'dos_campari','Campari',15,'Dose de Campari.','50 ml',3,S)
it(c,'dos_seleta','Seleta',15,'Dose de cachaça Seleta.','50 ml',3,S,O['cachaca'])
it(c,'dos_asa_branca','Cachaça Asa Branca',10,'Dose de cachaça Asa Branca.','50 ml',3,S,O['cachaca'])
it(c,'dos_moicana','Cachaça Moicana Ouro',12,'Dose de cachaça Moicana Ouro.','50 ml',3,S,O['cachaca'])
it(c,'dos_pitu_51','Pitu ou 51',6,'Dose de cachaça Pitu ou 51.','50 ml',3,S,O['cachaca'])
it(c,'dos_bacardi','Bacardi',15,'Dose de rum Bacardi.','50 ml',3,S)
it(c,'dos_tequila','Tequila',25,'Dose de tequila.','50 ml',3,S)
S = 'Bebidas Quentes – Combos'
it(c,'bq_buchanans','Combo Whisky Buchanan\'s',400,QUENTE+' Buchanan\'s 12 anos.','Garrafa 1 L',5,S)
it(c,'bq_chivas','Combo Whisky Chivas Regal',300,QUENTE+' Chivas Regal 12 anos.','Garrafa 1 L',5,S)
it(c,'bq_old_parr','Combo Whisky Old Parr',380,QUENTE+' Old Parr 12 anos.','Garrafa 1 L',5,S)
it(c,'bq_red_label','Combo Whisky Red Label',200,QUENTE+' Johnnie Walker Red Label.','Garrafa 1 L',5,S)
it(c,'bq_gold_label','Combo Whisky Gold Label',470,QUENTE+' Johnnie Walker Gold Label.','Garrafa 1 L',5,S)
it(c,'bq_absolut','Combo Vodka Absolut',220,QUENTE+' Vodka Absolut.','Garrafa 1 L',5,S)
it(c,'bq_gin_tanqueray','Combo Gin Tanqueray',260,'Garrafa de Gin Tanqueray + 4 águas tônicas.','Garrafa 750 ml',5,S)
it(c,'bq_gin_beefeater','Combo Gin Beefeater',230,'Garrafa de Gin Beefeater + 4 águas tônicas.','Garrafa 750 ml',5,S)
it(c,'bq_gelo_coco','Gelo de Coco',8,'Gelo de coco para acompanhar sua bebida.','Pacote',3,S)
S = 'Espumantes & Vinhos'
it(c,'vin_chandon','Espumante Chandon',200,'Espumante Chandon gelado.','Garrafa 750 ml',5,S)
it(c,'vin_pergola','Vinho Pérgola',80,'Vinho Pérgola tinto ou branco.','Garrafa 750 ml',5,S)
it(c,'vin_quinta_morgado','Vinho Quinta do Morgado',80,'Vinho Quinta do Morgado tinto suave.','Garrafa 750 ml',5,S)
it(c,'vin_casillero','Casillero del Diablo',120,'Vinho Casillero del Diablo.','Garrafa 750 ml',5,S)

# ═════════════ SOBREMESAS & CONVENIÊNCIA ═════════════
c = cat('conveniencia', 'Sobremesas & Conveniência', '🍦'); S = 'Picolés'
P = A('picole.jpg')
for k, n, p in [('cookies','Cookies e Cream',18),('classico','Clássico',18),('avela','Leite e Creme de Avelã',16),
                ('belga','Chocolate Belga c/ Brigadeiro',16),('morango_leite','Morango c/ Leite Condensado',16),
                ('torta_limao','Torta de Limão',15),('mousse_maracuja','Mousse de Maracujá',15),('coco','Coco',15),
                ('pacoca','Paçoca',15),('morango','Morango',15),('choc_zero','Chocolate Zero',15)]:
    it(c,'pic_'+k,'Picolé '+n,p,f'Picolé artesanal sabor {n.lower()}.','1 unidade',2,S,P)
S = 'Conveniência'
for k, n, p in [('carlton','Carlton',20),('hollywood','Hollywood',18),('lucky','Lucky Strike',18),('isqueiro','Isqueiro',10),
                ('halls','Halls',5),('mentos','Mentos',5),('pop','Pirulito Pop Grande',4),('pirulito','Pirulito',2)]:
    it(c,'conv_'+k,n,p,n+'.','1 unidade',1,S)

# ---------- serializa ----------
def js(v):
    return json.dumps(v, ensure_ascii=False)
lines = ['const DEFAULT_CATEGORIAS = [']
for c in CATS:
    lines.append(f'  {{ id: {js(c["id"])}, nome: {js(c["nome"])}, icone: {js(c["icone"])}, itens: [')
    for i in c['itens']:
        lines.append('    { ' + ', '.join(f'{k}: {js(v)}' for k, v in i.items()) + '},')
    lines.append('  ]},')
block = '\n'.join(lines)

src = open(PATH, encoding='utf-8').read()
a = src.find('const DEFAULT_CATEGORIAS = ['); b = src.find('\n];', a)
assert a > 0 and b > a
src = src[:a] + block + src[b:]
# versao do cache local
src = re.sub(r'var VER="[^"]+";', 'var VER="gv_v15_beachfarol";', src, count=1)
# placeholder neutro no lugar da foto generica do unsplash
src = re.sub(r"https://images\.unsplash\.com/photo-1555939594-58d7cb561ad1\?w=\d+&q=\d+", NOIMG, src)
src = src.replace('String(savedIt.img).indexOf("photo-1555939594") === -1', 'String(savedIt.img).indexOf("sem-foto") === -1')
open(PATH, 'w', encoding='utf-8').write(src)
tot = sum(len(c['itens']) for c in CATS); semfoto = sum(1 for c in CATS for i in c['itens'] if i['img'] == NOIMG)
print('categorias', len(CATS), 'itens', tot, 'sem foto', semfoto)
ids = [i['id'] for c in CATS for i in c['itens']]; assert len(ids) == len(set(ids)), 'id duplicado'

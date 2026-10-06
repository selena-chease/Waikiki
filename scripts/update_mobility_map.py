import re
import xml.etree.ElementTree as ET
import sys

def get_cuba_group():
    with open('en/infrastructure.html', 'r', encoding='utf-8') as f:
        content = f.read()
    m = re.search(r'(<g class="cuba-archipelago" transform="translate\(75, 228\) scale\(0.82\)">.*?</g>)', content, re.DOTALL)
    if not m:
        raise ValueError("Could not find cuba-archipelago in en/infrastructure.html")
    return m.group(1)

def build_svg(lang="en", cuba_xml=""):
    is_hu = (lang == "hu")
    
    aria_label = (
        "Waikiki szigeti közlekedési folyosóinak sematikus térképe: Florida, Kuba és Haiti összeköttetései"
        if is_hu else
        "Schematic map of Waikiki transport corridors connecting Florida, Cuba, and Haiti"
    )
    
    # Florida titles
    t_fl_pan = "Florida Panhandle és Északnyugat" if is_hu else "Florida Panhandle"
    t_fl_north = "Észak-Florida és First Coast" if is_hu else "North Florida and First Coast"
    t_fl_central = "Közép-Florida és Űr-partvidék" if is_hu else "Central Florida and Space Coast"
    t_fl_west = "Tampa-öböl és Napsugár-part" if is_hu else "Tampa Bay and Suncoast"
    t_fl_south = "Dél-Florida és Miami" if is_hu else "South Florida and Miami"
    t_fl_glades = "Everglades és Florida-öböl" if is_hu else "Everglades and Florida Bay"
    
    # Keys titles
    t_k_largo = "Key Largo és Felső-szigetek" if is_hu else "Key Largo and Upper Keys"
    t_k_islamorada = "Islamorada és Középső-szigetek" if is_hu else "Islamorada and Middle Keys"
    t_k_marathon = "Marathon és Hétmérföldes ív" if is_hu else "Marathon and Seven Mile Arc"
    t_k_bigpine = "Big Pine és Alsó-szigetek" if is_hu else "Big Pine Key and Lower Keys"
    t_k_west = "Key West"
    t_k_marquesas = "Marquesas-szigetek" if is_hu else "Marquesas Keys"
    t_k_tortugas = "Dry Tortugas"
    
    # Haiti & Hispaniola titles
    t_ht_nw = "Haiti · Északnyugati megye (Môle Saint-Nicolas)" if is_hu else "Haiti · Nord-Ouest (Môle Saint-Nicolas)"
    t_ht_nord = "Haiti · Északi és Északkeleti megye (Cap-Haïtien)" if is_hu else "Haiti · Nord and Nord-Est (Cap-Haïtien)"
    t_ht_art = "Haiti · Artibonite és Központi-fennsík" if is_hu else "Haiti · Artibonite and Centre"
    t_ht_ouest = "Haiti · Nyugati megye és Port-au-Prince" if is_hu else "Haiti · Ouest and Port-au-Prince"
    t_ht_sud = "Haiti · Déli megye és Tiburon-félsziget" if is_hu else "Haiti · Sud and Tiburon Peninsula"
    t_ht_gonave = "Gonâve-sziget" if is_hu else "Île de la Gonâve"
    t_ht_tortuga = "Tortuga-sziget (Teknős-sziget)" if is_hu else "Île de la Tortue (Tortuga)"
    t_ht_vache = "Tehén-sziget (Île-à-Vache)" if is_hu else "Île-à-Vache"
    
    t_do_cibao = "Dominikai Köztársaság · Cibao és Északi partvidék" if is_hu else "Dominican Republic · Cibao and North Coast"
    t_do_sur = "Dominikai Köztársaság · Santo Domingo és Déli partvidék" if is_hu else "Dominican Republic · Santo Domingo and South Coast"
    t_do_saona = "Saona-sziget" if is_hu else "Isla Saona"
    
    # Jamaica titles
    t_jm_cornwall = "Jamaica · Cornwall megye (Montego Bay és Negril)" if is_hu else "Jamaica · Cornwall County (Montego Bay and Negril)"
    t_jm_middlesex = "Jamaica · Middlesex megye (Ocho Rios és Portland Point)" if is_hu else "Jamaica · Middlesex County (Ocho Rios and Portland Point)"
    t_jm_surrey = "Jamaica · Surrey megye (Kingston és Kék-hegység)" if is_hu else "Jamaica · Surrey County (Kingston and Blue Mountains)"
    t_jm_palisadoes = "Port Royal és a Palisadoes-turzás" if is_hu else "Port Royal and The Palisadoes"
    t_jm_pedro = "Pedro-zátonyok" if is_hu else "Pedro Cays"
    
    # Legend labels
    lbl_maglev = "MAGLEV"
    lbl_hyperloop = "HYPERLOOP"
    lbl_tunnel = "ALAGÚT" if is_hu else "TUNNEL"
    lbl_mainline = "FŐVONAL" if is_hu else "MAIN LINE"
    lbl_maritime = "TENGERI ÚTVONAL" if is_hu else "MARITIME ROUTE"
    
    # Geographic labels
    g_florida = "FLORIDA"
    g_bahamas = "BAHAMA-SZIGETEK" if is_hu else "BAHAMAS"
    g_cuba = "KUBA" if is_hu else "CUBA"
    g_haiti = "HAITI"
    g_domrep = "DOMINIKAI KÖZTÁRSASÁG" if is_hu else "DOMINICAN REP."
    g_jamaica = "JAMAICA"
    g_islands = "PÁLMA · VILÁG · KAMÉLEON" if is_hu else "PALM · WORLD · CHAMELEON"
    g_corridor = "TENGERALATTI FOLYOSÓ" if is_hu else "UNDERSEA CORRIDOR"
    g_passage = "SZÉL FELŐLI ÁTJÁRÓ LINK" if is_hu else "WINDWARD PASSAGE LINK"

    # Assemble SVG text
    svg = f'''<svg class="ill" viewBox="0 0 1160 540" role="img" aria-label="{aria_label}">
                    <defs>
                        <clipPath id="rm-clip">
                            <rect width="1160" height="540" rx="28" />
                        </clipPath>
                    </defs>
                    <g clip-path="url(#rm-clip)">
                        <rect width="1160" height="540" class="f-sea3" />
                        <!-- Geographic Coordinate Grid -->
                        <g class="k-white" stroke-width="1" opacity=".3">
                            <path d="M0 135h1160M0 270h1160M0 405h1160M290 0v540M580 0v540M870 0v540" />
                        </g>
                        <!-- ==================== FLORIDA REGIONS ==================== -->
                        <g id="florida-mainland">
                            <!-- FL-PAN: Panhandle -->
                            <path class="f-sand province-path" d="M 20,0 L 168,0 C 168,16 167,32 166,48 C 162,50 156,54 150,56 C 142,59 135,66 128,67 C 120,68 112,65 104,61 C 96,57 88,54 78,51 C 66,48 52,44 38,40 C 28,37 22,35 20,34 Z" id="FL-PAN" title="{t_fl_pan}" />
                            <!-- FL-NORTH: North Florida and First Coast -->
                            <path class="f-sand province-path" d="M 168,0 L 248,0 C 251,12 253,24 255,36 C 257,44 260,52 263,60 C 264,64 263,67 260,70 C 250,71 236,71 222,72 C 210,73 198,75 188,76 C 183,71 178,63 174,56 C 170,51 168,49 166,48 C 167,32 168,16 168,0 Z" id="FL-NORTH" title="{t_fl_north}" />
                            <!-- FL-CENTRAL: Central Florida and Space Coast -->
                            <path class="f-sand province-path" d="M 188,76 C 198,75 210,73 222,72 C 236,71 250,71 260,70 C 263,67 264,64 263,60 C 266,66 272,74 276,80 C 278,84 278,88 276,94 C 274,102 272,112 271,122 C 262,125 252,129 242,134 C 238,131 232,126 226,122 C 218,117 210,111 204,104 C 198,96 193,87 188,76 Z" id="FL-CENTRAL" title="{t_fl_central}" />
                            <!-- FL-WEST: Tampa Bay and Suncoast -->
                            <path class="f-sand province-path" d="M 188,76 C 193,87 198,96 204,104 C 210,111 218,117 226,122 C 220,128 214,136 210,144 C 206,152 204,160 206,168 C 208,174 212,178 216,182 C 212,176 208,166 204,154 C 200,142 196,130 195,122 C 194,114 192,106 189,96 C 187,88 187,82 188,76 Z" id="FL-WEST" title="{t_fl_west}" />
                            <!-- FL-SOUTH: South Florida and Miami Gold Coast -->
                            <path class="f-sand province-path" d="M 271,122 C 270,132 268,144 267,156 C 266,166 265,174 264,180 C 262,186 258,192 254,195 C 251,192 249,186 248,180 C 247,172 248,164 249,154 C 250,146 251,138 252,130 C 258,127 265,124 271,122 Z" id="FL-SOUTH" title="{t_fl_south}" />
                            <!-- FL-GLADES: Everglades and Florida Bay -->
                            <path class="f-sand province-path" d="M 226,122 C 232,126 238,131 242,134 C 247,132 250,129 252,130 C 251,138 250,146 249,154 C 248,164 247,172 248,180 C 249,186 251,192 254,195 C 248,198 240,199 232,197 C 224,195 218,190 216,182 C 212,178 208,174 206,168 C 204,160 206,152 210,144 C 214,136 220,128 226,122 Z" id="FL-GLADES" title="{t_fl_glades}" />
                            <!-- Lake Okeechobee Freshwater Basin -->
                            <path class="f-sea3" d="M 238,138 C 244,134 250,136 252,141 C 254,146 251,152 247,155 C 242,157 236,155 234,149 C 233,144 235,140 238,138 Z" />
                        </g>
                        <!-- ==================== FLORIDA KEYS ==================== -->
                        <g id="florida-keys">
                            <path class="f-sand province-path" d="M 258,194 C 262,196 266,200 264,204 C 262,207 257,206 255,202 C 254,198 255,195 258,194 Z" id="FL-KEY-LARGO" title="{t_k_largo}" />
                            <path class="f-sand province-path" d="M 248,205 C 252,207 253,211 250,214 C 247,215 244,213 243,210 C 243,207 245,205 248,205 Z" id="FL-KEY-ISLAMORADA" title="{t_k_islamorada}" />
                            <path class="f-sand province-path" d="M 233,213 C 237,215 238,218 235,221 C 231,223 227,220 226,217 C 226,214 229,213 233,213 Z" id="FL-KEY-MARATHON" title="{t_k_marathon}" />
                            <path class="f-sand province-path" d="M 218,219 C 222,221 222,224 219,227 C 216,228 213,226 212,223 C 212,220 215,219 218,219 Z" id="FL-KEY-BIGPINE" title="{t_k_bigpine}" />
                            <path class="f-sand province-path" d="M 204,223 C 207,224 207,227 204,229 C 201,230 198,228 198,226 C 198,224 201,223 204,223 Z" id="FL-KEY-WEST" title="{t_k_west}" />
                            <path class="f-sand province-path" d="M 188,226 C 191,227 191,229 189,230 C 186,231 184,229 185,227 C 185,226 187,226 188,226 Z" id="FL-KEY-MARQUESAS" title="{t_k_marquesas}" />
                            <path class="f-sand province-path" d="M 174,227 C 176,227 176,229 174,230 C 172,230 171,229 171,228 C 171,227 173,227 174,227 Z" id="FL-KEY-TORTUGAS" title="{t_k_tortugas}" />
                        </g>
                        <!-- ==================== BAHAMAS ARCHIPELAGO ==================== -->
                        <g class="f-sand" opacity=".88">
                            <path d="M294 72 c16 -5 36 -6 49 -2 c4 2 2 6 -3 7 c-16 3 -36 2 -48 -2 c-4 -1 -2 -5 2 -5 z" />
                            <path d="M352 62 c8 2 13 10 11 18 c-2 9 -10 15 -14 12 c-3 -2 -1 -7 2 -12 c3 -5 3 -14 1 -18 z" />
                            <ellipse cx="292" cy="154" rx="4.5" ry="2.8" />
                            <circle cx="328" cy="118" r="3.2" />
                            <path d="M318 152 c9 -6 22 -4 26 5 c4 10 2 26 -4 37 c-6 11 -16 15 -21 9 c-5 -7 -3 -24 1 -35 c2 -8 1 -12 -2 -16 z" />
                            <circle cx="370" cy="176" r="3" />
                            <path d="M382 192 c12 -4 26 -2 32 4 c3 3 0 7 -4 7 c-12 1 -24 -2 -28 -6 z" />
                            <circle cx="430" cy="226" r="2.8" />
                        </g>
                        <!-- ==================== CUBA ARCHIPELAGO (DETAILED) ==================== -->
                        {cuba_xml}
                        <!-- Cuban Cays and Surrounding Archipelagos -->
                        <g class="f-sand" opacity=".92">
                            <!-- Jardines del Rey (North Coast Cays) -->
                            <path d="M370 248 a5 2.5 0 1 0 10 0 a5 2.5 0 1 0 -10 0" />
                            <path d="M424 256 a5 2.5 0 1 0 10 0 a5 2.5 0 1 0 -10 0" />
                            <path d="M448 259 c6 -2 14 -1 18 2 c-4 3 -12 2 -18 -2 z" />
                            <path d="M488 268 c8 -2 18 0 22 4 c-5 3 -15 2 -22 -4 z" />
                            <path d="M536 284 a7 3 0 1 0 14 0 a7 3 0 1 0 -14 0" />
                            <!-- Los Canarreos and Jardines de la Reina (South Coast Cays) -->
                            <path d="M262 346 c8 -2 18 1 20 5 c-6 3 -16 1 -20 -5 z" />
                            <ellipse cx="236" cy="342" rx="4" ry="2.5" />
                            <path d="M430 355 c12 6 26 14 38 18 c-10 -2 -24 -8 -38 -18 z" />
                            <path d="M475 375 c12 6 24 12 36 16 c-10 -2 -22 -7 -36 -16 z" />
                        </g>
                        <!-- Cayman Islands (South of Cuba) -->
                        <g class="f-sand" opacity=".85">
                            <!-- Grand Cayman -->
                            <path d="M320 405 c6 -2 14 0 18 3 c-3 2 -11 2 -16 -1 z" />
                            <!-- Little Cayman and Cayman Brac -->
                            <circle cx="362" cy="392" r="2" />
                            <ellipse cx="376" cy="388" rx="3.5" ry="1.6" />
                        </g>
                        <!-- Waikiki Artificial Archipelagos (Palm, World, Chameleon) -->
                        <g class="f-sand">
                            <!-- The Palm Island -->
                            <path d="M226 276 c-4 -6 6 -9 11 -6 c5 3 4 8 -2 9 c-3 1 -6 -1 -7 -2 z" />
                            <circle cx="230" cy="272" r="3.2" />
                            <circle cx="224" cy="272" r="2.8" />
                            <!-- The World Archipelago -->
                            <circle cx="210" cy="290" r="2.4" />
                            <circle cx="216" cy="289" r="2.2" />
                            <circle cx="212" cy="295" r="2.6" />
                            <circle cx="218" cy="294" r="2.2" />
                            <circle cx="215" cy="298" r="1.8" />
                            <!-- Chameleon Island -->
                            <path d="M232 296 c3 -3 8 -3 11 0 c2 2 3 5 1 7 c-2 2 -6 2 -8 1 c-3 -1 -4 3 -2 4 c2 1 5 0 6 -1 c-1 3 -4 4 -6 3 c-3 -2 -4 -6 -2 -8 c1 -2 0 -4 -1 -5 z" />
                            <circle cx="240" cy="297" r="1.2" class="f-white" />
                        </g>
                        <!-- ==================== JAMAICA (DETAILED COUNTIES) ==================== -->
                        <g id="jamaica-regions">
                            <!-- JM-CORNWALL: Cornwall County (West) -->
                            <path class="f-sand province-path" d="M 526,488 C 530,482 538,477 548,474 C 556,472 562,475 566,480 L 568,498 C 560,501 550,501 540,498 C 532,495 526,492 526,488 Z" id="JM-CORNWALL" title="{t_jm_cornwall}" />
                            <!-- JM-MIDDLESEX: Middlesex County (Central) -->
                            <path class="f-sand province-path" d="M 566,480 C 574,475 586,474 600,475 C 610,476 618,479 622,484 L 624,502 C 614,506 606,514 596,512 C 586,510 578,504 568,498 L 566,480 Z" id="JM-MIDDLESEX" title="{t_jm_middlesex}" />
                            <!-- JM-SURREY: Surrey County (East and Kingston) -->
                            <path class="f-sand province-path" d="M 622,484 C 628,480 638,480 648,483 C 658,487 664,491 664,494 C 660,499 652,501 642,502 C 632,502 626,501 624,502 L 622,484 Z" id="JM-SURREY" title="{t_jm_surrey}" />
                            <!-- Port Royal and The Palisadoes Spit -->
                            <path class="f-sand province-path" d="M 622,501 C 628,502 636,503 640,501 C 641,500 638,498 632,498 C 626,499 622,500 622,501 Z" id="JM-PALISADOES" title="{t_jm_palisadoes}" />
                            <!-- Pedro Cays -->
                            <path class="f-sand province-path" d="M 584,528 C 588,527 592,528 594,530 C 592,532 588,531 584,528 Z" id="JM-PEDRO" title="{t_jm_pedro}" />
                        </g>
                        <!-- ==================== HISPANIOLA (HAITI AND DOMINICAN REP. DETAILED) ==================== -->
                        <g id="hispaniola-regions">
                            <!-- HT-NW: Nord-Ouest -->
                            <path class="f-sand province-path" d="M 752,338 C 762,334 778,332 796,330 C 804,337 810,346 816,354 C 820,360 822,364 818,366 C 804,367 790,364 776,358 C 764,352 754,344 752,338 Z" id="HT-NW" title="{t_ht_nw}" />
                            <!-- HT-NORD: Nord and Nord-Est (Cap-Haïtien) -->
                            <path class="f-sand province-path" d="M 796,330 C 818,328 842,332 864,338 C 884,336 902,335 918,336 C 916,346 912,356 908,366 C 892,365 874,364 856,362 C 836,360 824,358 816,354 C 810,346 804,337 796,330 Z" id="HT-NORD" title="{t_ht_nord}" />
                            <!-- HT-ART: Artibonite and Centre -->
                            <path class="f-sand province-path" d="M 818,366 C 822,364 820,360 816,354 C 824,358 836,360 856,362 C 874,364 892,365 908,366 C 910,378 914,392 918,406 C 904,408 888,409 874,408 C 864,398 854,386 842,378 C 832,372 824,368 818,366 Z" id="HT-ART" title="{t_ht_art}" />
                            <!-- HT-OUEST: Ouest and Port-au-Prince -->
                            <path class="f-sand province-path" d="M 874,408 C 888,409 904,408 918,406 C 922,418 924,430 926,442 C 914,444 898,443 884,440 C 876,432 872,422 870,416 C 871,412 873,410 874,408 Z" id="HT-OUEST" title="{t_ht_ouest}" />
                            <!-- HT-SUD: Sud, Grand'Anse and Nippes (Tiburon Peninsula) -->
                            <path class="f-sand province-path" d="M 744,438 C 758,432 776,430 798,430 C 820,430 844,432 866,435 C 870,437 876,440 884,440 C 898,443 914,444 926,442 C 926,448 924,452 920,454 C 900,453 876,450 852,448 C 824,452 796,455 776,453 C 760,450 748,446 744,438 Z" id="HT-SUD" title="{t_ht_sud}" />
                            <!-- HT-GONAVE: Île de la Gonâve -->
                            <path class="f-sand province-path" d="M 826,410 C 838,404 854,405 864,411 C 869,415 867,421 860,424 C 848,427 834,425 826,419 C 822,415 822,412 826,410 Z" id="HT-GONAVE" title="{t_ht_gonave}" />
                            <!-- HT-TORTUGA: Île de la Tortue (Tortuga) -->
                            <path class="f-sand province-path" d="M 810,324 C 822,320 836,321 846,325 C 850,328 848,332 842,333 C 830,335 818,334 810,329 C 807,327 807,325 810,324 Z" id="HT-TORTUGA" title="{t_ht_tortuga}" />
                            <!-- HT-VACHE: Île-à-Vache -->
                            <path class="f-sand province-path" d="M 778,455 C 782,453 787,454 789,457 C 789,459 786,461 782,460 C 778,459 776,457 778,455 Z" id="HT-VACHE" title="{t_ht_vache}" />
                            <!-- DO-CIBAO: Dominican Republic · North and Cibao -->
                            <path class="f-sand province-path" d="M 918,336 C 946,334 984,332 1024,334 C 1068,336 1114,340 1160,346 L 1160,392 C 1118,390 1072,388 1028,386 C 980,384 942,386 918,388 C 914,374 910,360 908,366 C 912,356 916,346 918,336 Z" id="DO-CIBAO" title="{t_do_cibao}" />
                            <!-- DO-SUR: Dominican Republic · South and Santo Domingo -->
                            <path class="f-sand province-path" d="M 918,388 C 942,386 980,384 1028,386 C 1072,388 1118,390 1160,392 L 1160,446 C 1120,444 1074,440 1028,438 C 984,438 950,444 926,442 C 924,430 922,418 918,406 C 914,392 910,378 918,388 Z" id="DO-SUR" title="{t_do_sur}" />
                            <!-- DO-SAONA: Isla Saona -->
                            <path class="f-sand province-path" d="M 1128,450 C 1135,448 1142,450 1145,453 C 1145,456 1139,458 1133,456 C 1128,454 1126,451 1128,450 Z" id="DO-SAONA" title="{t_do_saona}" />
                        </g>
                        <!-- ==================== TRANSPORT CORRIDORS ==================== -->
                        <!-- Florida Undersea Corridor: Miami to Nova Aurelia via Keys -->
                        <path d="M265 178 C255 198, 235 218, 202 225 C186 248, 214 274, 255 292" class="k-ink" stroke-width="4.5" stroke-dasharray="2 7" stroke-linecap="round" />
                        <!-- Trans-Cuba Main Line: Nova Aurelia to Morón -->
                        <path d="M255 292 C285 272, 360 266, 458 273" class="k-ink2" stroke-width="4.5" stroke-linecap="round" />
                        <!-- Hyperloop: Nova Aurelia to Mega Pyramid City -->
                        <path d="M255 292 L290 264" class="k-gold" stroke-width="5.5" stroke-linecap="round" />
                        <!-- High-Speed Maglev: Morón to Port Royal and Santiago -->
                        <path d="M458 273 C500 295, 525 320, 540 340 C560 365, 580 395, 598 419" class="k-coral" stroke-width="5.5" stroke-linecap="round" />
                        <!-- Windward Passage Link: Santiago to Cap-Haïtien and Port-au-Prince -->
                        <path d="M598 419 C645 428, 690 422, 730 395 C780 360, 820 345, 862 340" class="k-coral" stroke-width="5.5" stroke-linecap="round" />
                        <path d="M862 340 C882 370, 895 400, 908 432" class="k-coral" stroke-width="5.5" stroke-linecap="round" />
                        <!-- Jamaica Maritime Express Link: Santiago to Kingston and Montego Bay -->
                        <path d="M598 419 C610 445, 622 470, 630 498" class="k-sea" stroke-width="3.5" stroke-dasharray="3 6" stroke-linecap="round" />
                        <path d="M255 292 C320 370, 440 435, 556 474" class="k-sea" stroke-width="2.8" stroke-dasharray="3 6" stroke-linecap="round" opacity=".75" />
                        <!-- Island Elevated Link to Artificial Islands -->
                        <path d="M255 292 C245 294, 235 296, 226 288" class="k-ink2" stroke-width="2.8" stroke-dasharray="4 4" />
                        <!-- Animated Traffic Dots -->
                        <circle r="5" class="f-white">
                            <animateMotion dur="5.5s" repeatCount="indefinite" path="M265 178 C255 198, 235 218, 202 225 C186 248, 214 274, 255 292" />
                        </circle>
                        <circle r="4.5" class="f-white">
                            <animateMotion dur="4.5s" repeatCount="indefinite" path="M255 292 C285 272, 360 266, 458 273" />
                        </circle>
                        <circle r="4" class="f-white">
                            <animateMotion dur="1.8s" repeatCount="indefinite" path="M255 292 L290 264" />
                        </circle>
                        <circle r="5" class="f-white">
                            <animateMotion dur="4.2s" repeatCount="indefinite" path="M458 273 C500 295, 525 320, 540 340 C560 365, 580 395, 598 419" />
                        </circle>
                        <circle r="5" class="f-white">
                            <animateMotion dur="5.5s" repeatCount="indefinite" path="M598 419 C645 428, 690 422, 730 395 C780 360, 820 345, 862 340" />
                        </circle>
                        <circle r="4.5" class="f-white">
                            <animateMotion dur="3.6s" repeatCount="indefinite" path="M862 340 C882 370, 895 400, 908 432" />
                        </circle>
                        <circle r="4" class="f-white">
                            <animateMotion dur="6.0s" repeatCount="indefinite" path="M598 419 C610 445, 622 470, 630 498" />
                        </circle>
                        <!-- ==================== CAPITAL AND STATIONS ==================== -->
                        <!-- Capital City Marker: Nova Aurelia (Southern shores of Waikiki) -->
                        <g>
                            <circle cx="255" cy="292" r="16" class="f-coral pulse" />
                            <circle cx="255" cy="292" r="11" class="f-coral" />
                            <path d="M255 285 l2 4.2 4.6.6 -3.4 3.2 .9 4.5 -4.1 -2.2 -4.1 2.2 .9 -4.5 -3.4 -3.2 4.6 -.6 z" class="f-white" />
                        </g>
                        <!-- Station Network Nodes -->
                        <g class="f-ink">
                            <circle cx="265" cy="178" r="7" />
                            <circle cx="202" cy="225" r="5.5" />
                            <circle cx="290" cy="264" r="6" />
                            <circle cx="458" cy="273" r="7" />
                            <circle cx="540" cy="340" r="5.5" />
                            <circle cx="598" cy="419" r="7" />
                            <circle cx="862" cy="340" r="7" />
                            <circle cx="908" cy="432" r="7" />
                            <circle cx="630" cy="498" r="6" />
                            <circle cx="556" cy="474" r="5.5" />
                        </g>
                        <!-- Mega Pyramid Mark -->
                        <path d="M290 255 l4 7 h-8 z" class="f-gold" />
                        <g class="f-white">
                            <circle cx="265" cy="178" r="2.8" />
                            <circle cx="202" cy="225" r="2.2" />
                            <circle cx="290" cy="264" r="2.2" />
                            <circle cx="458" cy="273" r="2.8" />
                            <circle cx="540" cy="340" r="2.2" />
                            <circle cx="598" cy="419" r="2.8" />
                            <circle cx="862" cy="340" r="2.8" />
                            <circle cx="908" cy="432" r="2.8" />
                            <circle cx="630" cy="498" r="2.4" />
                            <circle cx="556" cy="474" r="2.2" />
                        </g>
                        <!-- ==================== TYPOGRAPHY AND LABELS ==================== -->
                        <g font-size="11.5">
                            <text x="255" y="322" text-anchor="middle" font-size="13.5" font-weight="700">NOVA AURELIA</text>
                            <text x="278" y="178" font-size="12" font-weight="600">MIAMI</text>
                            <text x="195" y="238" font-size="9.5" text-anchor="end">KEY WEST</text>
                            <text x="302" y="260" font-size="10.5" font-weight="600">MEGA PYRAMID CITY</text>
                            <text x="458" y="260" text-anchor="middle" font-size="12" font-weight="600">MORÓN</text>
                            <text x="552" y="340" font-size="10">PORT ROYAL</text>
                            <text x="598" y="438" text-anchor="middle" font-size="12" font-weight="600">SANTIAGO</text>
                            <text x="862" y="328" text-anchor="middle" font-size="12" font-weight="600">CAP-HAÏTIEN</text>
                            <text x="922" y="436" font-size="12" font-weight="600">PORT-AU-PRINCE</text>
                            <text x="642" y="512" font-size="10.5" font-weight="600">KINGSTON</text>
                            <text x="548" y="468" font-size="9.5" font-weight="600" text-anchor="end">MONTEGO BAY</text>
                            <!-- Major Territories -->
                            <text x="210" y="70" font-size="13" font-weight="600" opacity=".6" letter-spacing=".15em">{g_florida}</text>
                            <text x="365" y="115" font-size="11" font-weight="600" opacity=".45" letter-spacing=".15em">{g_bahamas}</text>
                            <text x="360" y="306" font-size="15" font-weight="600" opacity=".5" letter-spacing=".22em">{g_cuba}</text>
                            <text x="825" y="380" font-size="14" font-weight="600" opacity=".5" letter-spacing=".22em">{g_haiti}</text>
                            <text x="980" y="365" font-size="12" font-weight="600" opacity=".4" letter-spacing=".18em">{g_domrep}</text>
                            <text x="595" y="492" font-size="11" opacity=".55" letter-spacing=".15em" text-anchor="middle">{g_jamaica}</text>
                            <text x="145" y="298" font-size="9" text-anchor="middle">{g_islands}</text>
                            <text x="210" y="246" font-size="9" opacity=".8" font-weight="600" transform="rotate(58 210 246)">{g_corridor}</text>
                            <text x="760" y="378" font-size="9.5" opacity=".8" font-weight="600" transform="rotate(-24 760 378)">{g_passage}</text>
                        </g>
                        <!-- ==================== MAP LEGEND BOX ==================== -->
                        <g transform="translate(810 448)" font-size="10">
                            <rect x="-14" y="-12" width="314" height="70" rx="12" class="f-white" opacity=".92" />
                            <path d="M0 2h26" class="k-coral" stroke-width="5" stroke-linecap="round" /><text x="34" y="5.5" font-weight="600">{lbl_maglev}</text>
                            <path d="M125 2h26" class="k-gold" stroke-width="5" stroke-linecap="round" /><text x="159" y="5.5" font-weight="600">{lbl_hyperloop}</text>
                            <path d="M0 26h26" class="k-ink" stroke-width="4" stroke-dasharray="2 7" stroke-linecap="round" /><text x="34" y="29.5" font-weight="600">{lbl_tunnel}</text>
                            <path d="M125 26h26" class="k-ink2" stroke-width="4" stroke-linecap="round" /><text x="159" y="29.5" font-weight="600">{lbl_mainline}</text>
                            <path d="M0 46h26" class="k-sea" stroke-width="3" stroke-dasharray="3 6" stroke-linecap="round" /><text x="34" y="49.5" font-weight="600">{lbl_maritime}</text>
                        </g>
                    </g>
                </svg>'''
    return svg

def main():
    cuba_group = get_cuba_group()
    print("Found Cuba group, size:", len(cuba_group))
    
    for lang, filepath in [("en", "en/infrastructure.html"), ("hu", "hu/infrastructure.html")]:
        svg_content = build_svg(lang, cuba_group)
        
        # Validate XML parsing
        try:
            ET.fromstring(svg_content)
            print(f"[{lang}] SVG parsed successfully as valid XML!")
        except Exception as e:
            print(f"[{lang}] XML parse error:", e)
            sys.exit(1)
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Locate figure inside #mobility
        mob_idx = content.find('id="mobility"')
        fig_str = '<figure class="ill-panel" data-reveal="zoom">'
        fig_idx = content.find(fig_str, mob_idx)
        cap_str = '<figcaption class="ill-caption">'
        cap_idx = content.find(cap_str, fig_idx)
        
        if mob_idx == -1 or fig_idx == -1 or cap_idx == -1:
            raise ValueError(f"Could not locate mobility figure boundaries in {filepath}")
            
        # Replace the SVG inside figure
        before = content[:fig_idx + len(fig_str)]
        after = content[cap_idx:]
        
        new_content = before + "\n                " + svg_content + "\n                " + after
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath} successfully!")

if __name__ == '__main__':
    main()

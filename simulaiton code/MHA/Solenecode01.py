from main import * 
import math
import shutil
import os

chemin_fichier_xml='/home/solene/Bureau/case1/param.xml' 
sim = SimulationCouplee(chemin_fichier_xml) #initialisation

########################
### calculs solaires ### 
########################
sim.SolCommand.param['latitude'] = 48.785
sim.SolCommand.param['longitude'] = 2.474

##############################################
### insert the meteo file (radiation file) ### 
##############################################
meteo_folder = '/media/sf_SharedVBox/meteo Juin/' #copypaste your meteo file into ciel folder
destination_folder = '/home/solene/Bureau/simulation/simulSol/ciel/'
for filename in os.listdir(meteo_folder):
    meteo_file = os.path.join(meteo_folder,filename)
    dst_file = os.path.join(destination_folder,filename)
    if os.path.isfile(meteo_file):
        shutil.copy2(meteo_file, dst_file)

sim.solEnv.creer_descripteur_solaires()
sim.SolCommand.calculer_luminance_ciel()
sim.SolCommand.calculer_flux_solaires(fichier_meteo=True)
sim.solEnv.supprimer_nan(sim.SolCommand.chemin_clo+'/flux_sol_diffus')
sim.solEnv.supprimer_nan(sim.SolCommand.chemin_clo+'/flux_sol_direct')
sim.solEnv.supprimer_nan(sim.SolCommand.chemin_clo+'/flux_sol_total')
sim.SolCommand.calculer_fac_form()
sim.SolCommand.calculer_fac_form_ciel()
sim.SolCommand.calculer_radiosite()
liste_radiation = ['ecl_abs_total', 'ecl_diffus', 'ecl_inc_total', 'ecl_ref_total', 'flux_sol_diffus', 'flux_sol_direct', 'flux_sol_total']
sim.solEnv.recuperer_resultat(lst_var = liste_radiation)

############### 01: Wind speed model ###############
# This function currently implements simplified models that only consider wind speed #
############### 01: Wind speed model ###############
def calculer_hc(v):
    hc = 3.8*v + 5.7
    return hc

##################################
### wind speed transformation ### 
##################################
def wind_speed_at_height(u1, z1, z2, z0):
    u = u1*(math.log(z2/z0)/math.log(z1/z0))
    if u < 0.5:
        return 0.5
    else:
        return u

z0 = 0.4 #surface roughness

#####################################
### creation des fichiers necessaire au calcul thermoradiatif ### 
#####################################
sim.solEnv.definir_meteo_liste(sim.meteo_liste) 
sim.solEnv.creer_descripteur_veg() 
sim.solEnv.creer_param_simulation_ts(T_init = 22, hc = 10) 
sim.solEnv.creer_evaporation()

####################################################
## Chemin vers l'executable de simulation thermoradiative ## 
## Le chemin entier est necessaire si il est place dans un repertoire en dehors du PATH ## 
#################################################### 
nom_commande = 'simulation_Ts_EnergieBat_new.exe' 

###########################
### pas de temps 'zero' : initialisation ### 
###########################
v0 = wind_speed_at_height(sim.meteo_liste[0]['v'], 3, 10, z0)
sim.solEnv.creer_param_simulation_ts(hc = calculer_hc(v0))
sim.solEnv.definir_meteo(0,veg=True) 
sim.SolCommand.simulation_Ts_EnergieBat_new('init', # suffixe pour le pas de temps precedent 'init' 
    sim.TimeStep.liste_ts_sol[0], # suffixe pour le pas de temps du calcul 
    simulation_batiment = False, # utilisation ou non de simulation de lenergetique du batiment 
    simulation_vegetation = True, # utilisation ou non de model nodal pour la vegetation 
    meteo = True, # utilisation des parametre meteo pour les flux IR atmospherique
    nom_commande = nom_commande, # nom de l'executable pour la simulation thermoradiative
    terminal = True) # affichage de la sortie standart dans le terminal 

#############################
### pas de temps suivants ### 
#############################
for i in range(1, len(sim.TimeStep.liste_ts_sol)):
    vi = wind_speed_at_height(sim.meteo_liste[i]['v'], 3, 10, z0)
    sim.solEnv.creer_param_simulation_ts(hc = calculer_hc(vi)) 
    sim.solEnv.definir_meteo(i,veg=True) 
    avant = sim.TimeStep.liste_ts_sol[i-1]
    apres = sim.TimeStep.liste_ts_sol[i] 
    sim.SolCommand.simulation_Ts_EnergieBat_new(avant, 
                                                apres, 
                                                simulation_batiment = False, 
                                                simulation_vegetation = True, 
                                                meteo = True, 
                                                nom_commande = nom_commande) 
    print '\t sim_ts : de %s a %s' % (avant, apres)

from vtkFile import*
sim.solEnv.exporter_vtu(sim.post+'/resu_simu')

write_vtu_face(sim.geom_sol,sim.post+'/resu_simu_face.vtu')

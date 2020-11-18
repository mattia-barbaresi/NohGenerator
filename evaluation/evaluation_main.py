import os
from datetime import datetime

from numpy import average
from pandas import DataFrame

import random_individuals
import ritchie_criteria
from evaluation import *
from genetic_algorithm import constants, json_editor
from sbc import *

alpha = 0.5
now = datetime.now()
filename = "results_" + now.strftime("%Y%m%d-%H.%M")
root = "../data/results"
ncd_full = []
sbc_rep = []
sbc_archive = []
sbc_res = []
avg_typ = []
min_typ = []
crit_2_total = []
crit_2_edited_total = []
index1 = []
index2 = []
std = []
max = []
min = []
mean = []
avg_fit_total = []
avg_nov_total = []
len_repertoire = []
tmin = []
ngen = []
fit_thres_ful = []
diss_thres_ful = []
len_res_full = []
gen_fitness_total = []
string_res_total = []

fitness_archive_total = []
full_ncd_archive_total = []
criterion1_archive_total = []
criterion2_archive_total = []
len_Arch_full = []
average_min_typicality_archive_total = []
min_typ_total = {}
full_ncd_total = {}
all_results = {}
nov_total = {}


def calculate_fitness_generations(path):
    gens = 0
    with open(os.path.join(path, "generations_serialized")) as mf:
        for ln in mf:
            if "fitness" in ln:
                gens = gens + 1
    mf.close()
    return gens


for path, subdirs, files in os.walk(root):

    for name in files:
        if "results_serialized" in name:
            # results part
            results_serialized = []
            results_length = 0
            # if "and" not in path:
            #     name_results = "results_serialized"

            with open(os.path.join(path, name)) as fp:
                for line in fp:
                    if line != "\n":
                        results_length = results_length + 1
                    results_serialized.append(line[:-1])
            # print results
            len_res_full.append(results_length)
            fp.close()

            tot_eval = {}
            avg_eval = 0
            n = 0
            count = 0
            avg_fit_results = 0
            avg_nov = 0
            results_complete = []
            repertoire = []
            repertoire_length = 0
            # calculate fitness generations
            gen_fitness = calculate_fitness_generations(path=path)
            gen_fitness_total.append(gen_fitness)

            # open the repertoire
            with open(os.path.join(path, "repertoire_serialized")) as fp:
                for line in fp:
                    if line != "\n":
                        repertoire_length = repertoire_length + 1
                        repertoire.append(line[:-1])
            fp.close()

            # read results dict
            results_dict = json_editor.read_dict(os.path.join(path, "results"))
            fit = []
            ncd_local = []
            string_rep = concatenate_items_to_string(repertoire)
            nov_local = []
            for x in results_dict["results"]:
                results_complete.append(x["ind"])
                avg_fit_results = avg_fit_results + x["value"][0]
                fit.append(x["value"][0])
                ncd_local.append(compute_ncd("".join(x["ind"]), string_rep))
                if "and" in path:
                    avg_nov = avg_nov + x["value"][1]
                    nov_local.append(x["value"][1])
            all_results["alg"] = fit
            full_ncd_total["alg"] = ncd_local
            avg_fit_results = avg_fit_results / results_length
            avg_nov = avg_nov / results_length
            nov_total["full"] = nov_local

            avg_fit_total.append(avg_fit_results)
            avg_nov_total.append(avg_nov)
            crit1 = ritchie_criteria.compute_criterion_1(results=results_complete, string_repertoire=string_rep)
            crit2 = ritchie_criteria.compute_criterion_2(results=results_complete, string_repertoire=string_rep,
                                                         alpha=0.5)

            # sbc
            sbc_rep.append(compute_sbc(os.path.join(path, "repertoire_serialized")))
            sbc_res.append(compute_sbc(os.path.join(path, "results_serialized")))

            string_res = create_string_results(results_complete)
            string_res_total.append(string_res)
            tot_eval[string_res] = compute_ncd(string_res, string_rep)
            ncd_full.append(tot_eval[string_res])
            len_repertoire.append(repertoire_length)
            ngen.append(results_dict["parameters"]["generations"])
            tmin.append(results_dict["parameters"]["t_min "])
            fit_thres_ful.append(results_dict["parameters"]["fitness_threshold"])
            diss_thres_ful.append(results_dict["parameters"]["dissim_threshold"])
            tot_eval["average_typicality Criterion1"] = crit1
            avg_typ.append(crit1)
            tot_eval["min_typicality"] = calculate_typicality_with_min_distance_from_files(results=results_complete,
                                                                                       repertoire=repertoire)
            min_typ_total["alg"] = calculate_typicality_with_min_distance_from_files(results=results_complete,
                                                                                     repertoire=repertoire)
            min_typ.append(average(tot_eval["min_typicality"]))
            tot_eval["criterion2"] = crit2

            crit_2_total.append(crit2)
            index1.append(path.split("\\")[1])
            index2.append(path.split("\\")[2])
            # jsonEditor.dumpDict(os.path.join(path, filename), tot_eval)
            # here I have all the directories with results

            # archive part
            results_complete_archive = 0
            if results_dict["evaluation_method"] != "fitness":
                results_complete_archive = json_editor.read_dict(os.path.join(path, "res_arch"))
            if ("novelty" in path) and len(results_complete_archive.values()) > 0:
                results_archive = []
                avg_fit_archive = 0
                archive_string_complete = ""
                fitness_Arch = []
                ncd_local = []
                nov_local = []

                # sbc archive
                sbc_archive.append(compute_sbc(os.path.join(path, "archive_serialized")))

                for x in results_complete_archive.values():
                    results_archive.append(["choreo"])
                    archive_string_complete = archive_string_complete + "".join(x["choreo"])
                    avg_fit_archive = avg_fit_archive + x["fitness"]
                    fitness_Arch.append(x["fitness"])
                    ncd_local.append(compute_ncd("".join(x["choreo"]), string_rep))
                    nov_local.append(x["dissim"])
                nov_total["arch"] = nov_local

                full_ncd_total["archive"] = ncd_local
                all_results["archive"] = fitness_Arch
                min_typ_total["archive"] = calculate_typicality_with_min_distance_from_files(
                    results=results_archive, repertoire=repertoire)

                avg_fit_archive = avg_fit_archive / len(results_complete_archive.values())

                fitness_archive_total.append(avg_fit_archive)
                average_min_typicality_archive_total.append(average(
                    calculate_typicality_with_min_distance_from_files(results=results_archive,
                                                                      repertoire=repertoire)))
                criterion1_archive_total.append(
                    ritchie_criteria.compute_criterion_1(results=results_archive, string_repertoire=string_rep))
                criterion2_archive_total.append(
                    ritchie_criteria.compute_criterion_2(results=results_archive, string_repertoire=string_rep,
                                                         alpha=0.5))
                full_ncd_archive_total.append(compute_ncd(archive_string_complete, string_rep))
                len_Arch_full.append(len(results_complete_archive.values()))
            else:
                if "novelty" in path:
                    print "WARNING - no archive found in path: " + path
                fitness_archive_total.append("")
                full_ncd_archive_total.append("")
                criterion1_archive_total.append("")
                criterion2_archive_total.append("")
                average_min_typicality_archive_total.append("")
                len_Arch_full.append("")
                sbc_archive.append("")

            # random
            rand_ind = ""
            rand_ind_list = []
            ncd_local = []
            sbc_rnd = []
            for x in range(results_length):
                ind = random_individuals.init_individual(constants.NUMBER_OF_MOVES, constants.LIST_OF_MOVES.keys())
                rand_ind = rand_ind + "".join(ind)
                sbc_rnd.append("".join(ind))
                rand_ind_list.append(ind)
                ncd_local.append(compute_ncd("".join(ind), string_rep))
            index1.append(path.split("\\")[1])
            full_ncd_total["random"] = ncd_local

            # sbc for random
            sbc = SBC("bz2", "9", sbc_rnd)
            sbc_res.append(sbc.compute())
            sbc_rep.append("")
            sbc_archive.append("")

            index2.append("random")
            ncd_full.append(compute_ncd(rand_ind, string_rep))
            min_typ_total["random"] = calculate_typicality_with_min_distance_from_files(results=rand_ind_list,
                                                                                        repertoire=repertoire)
            min_typ.append(average(
                calculate_typicality_with_min_distance_from_files(results=rand_ind_list, repertoire=repertoire)))
            crit_1_rand = ritchie_criteria.compute_criterion_1(results=rand_ind_list, string_repertoire=string_rep)
            crit_2_rand = ritchie_criteria.compute_criterion_2(results=rand_ind_list, string_repertoire=string_rep,
                                                               alpha=0.5)
            evaluation_random_average = 0
            fit = []
            for ind in rand_ind_list:
                evaluation_rand = 0
                for x in repertoire:
                    # print "".join(ind), "".join(x)
                    evaluation_rand = evaluation_rand + string_similarity("".join(ind), "".join(x))
                evaluation_rand = evaluation_rand / repertoire_length
                evaluation_random_average = evaluation_random_average + evaluation_rand
                fit.append(evaluation_rand)
            all_results["random"] = fit
            evaluation_random_average = evaluation_random_average / len(rand_ind)
            avg_typ.append(crit_1_rand)
            crit_2_total.append(crit_2_rand)
            avg_fit_total.append(evaluation_random_average)
            len_res_full.append(results_length)
            tmin.append("")
            len_repertoire.append(repertoire_length)
            ngen.append("")
            gen_fitness_total.append("")
            fit_thres_ful.append("")
            diss_thres_ful.append("")
            string_res_total.append(rand_ind)
            fitness_archive_total.append("")
            full_ncd_archive_total.append("")
            criterion1_archive_total.append("")
            criterion2_archive_total.append("")
            average_min_typicality_archive_total.append("")
            avg_nov_total.append("")
            len_Arch_full.append("")

df = DataFrame({
    '01_parameters': index1,
    "02_method": index2,
    "03_ncd_full": ncd_full,
    "031_sbc_rep": sbc_rep,
    "032_sbc_archive": sbc_archive,
    "033_sbc_res": sbc_res,
    '04_criterion 1': avg_typ,
    '05_average min_typicality': min_typ,
    "06_avg_fit": avg_fit_total,
    '07_criterion 2 with ncd': crit_2_total,
    "08_len_Arch": len_Arch_full,
    "09_full ncd archive": full_ncd_archive_total,
    "10_criterion 1 archive": criterion1_archive_total,
    "11_ fitness archive average": fitness_archive_total,
    "12_criterion 2 archive": criterion2_archive_total,
    "13_average min typicality archive": average_min_typicality_archive_total,
    "14_gen_fitness": gen_fitness_total,
    "15_average novelty": avg_nov_total,
    "16_fit thresh": fit_thres_ful,
    "17_diss thresh": diss_thres_ful,
    "18_ngen": ngen,
    "19_tmin": tmin,
    "20_lenrep": len_repertoire,
    "21_len_res": len_res_full,
    "22_string_res": string_res_total,
})
df.to_excel("../data/results/" + filename + ".xlsx", sheet_name='sheet1', index=False)

import os
from datetime import datetime

from numpy import average
from pandas import DataFrame

import random_individuals
import ritchie_criteria
from evaluation import *
from genetic_algorithm import constants
from utils import json_editor
from sbc import *

alpha = 0.5
dir_n = "65_80"
root = "../data/results/" + dir_n
filename = "results_" + dir_n + "_" + datetime.now().strftime("%Y%m%d-%H.%M")

ncd_full = []
sbc_rep = []
sbc_archive = []
sbc_res = []
crit_1_total = []
min_typ = []
crit_2_total = []
index1 = []
index2 = []
std = []
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
all_results = {}


def calculate_fitness_generations(fpath):
    gens = 0
    with open(os.path.join(fpath, "generations_serialized")) as mf:
        for ln in mf:
            if "fitness" in ln:
                gens = gens + 1
    mf.close()
    return gens


for path, subdirs, files in os.walk(root):
    for name in files:
        if "results_serialized" in name:
            results_serialized = []
            results_length = 0
            with open(os.path.join(path, name)) as fp:
                for line in fp:
                    if line != "\n":
                        results_length = results_length + 1
                        results_serialized.append(line[:-1])
            len_res_full.append(results_length)
            fp.close()

            tot_eval = {}
            n = 0
            avg_fit_results = 0
            avg_nov = 0
            results_complete = []
            repertoire = []
            repertoire_length = 0
            # calculate fitness generations
            gen_fitness_total.append(calculate_fitness_generations(fpath=path))

            # open the repertoire
            with open(os.path.join(path, "repertoire_serialized")) as fp:
                for line in fp:
                    if line != "\n":
                        repertoire_length = repertoire_length + 1
                        repertoire.append(line[:-1])
            fp.close()

            # read results dict
            results_dict = json_editor.read_dict(os.path.join(path, "results"))
            string_rep = create_string(repertoire)
            fit = []
            nov_local = []
            for x in results_dict["results"]:
                results_complete.append(x["ind"])
                avg_fit_results = avg_fit_results + x["value"][0]
                fit.append(x["value"][0])
                if "novelty" in path:
                    avg_nov = avg_nov + x["value"][1]
                    nov_local.append(x["value"][1])
            all_results["alg"] = fit
            avg_fit_results = avg_fit_results / results_length
            avg_nov = avg_nov / results_length

            avg_fit_total.append(avg_fit_results)
            avg_nov_total.append(avg_nov)
            crit1 = ritchie_criteria.compute_criterion_1(results=results_complete, string_repertoire=string_rep)
            crit2 = ritchie_criteria.compute_criterion_2(results=results_complete, string_repertoire=string_rep,
                                                         alpha=0.5)

            # sbc
            sbc_rep.append(results_dict["sbc_rep"])
            sbc_res.append(results_dict["sbc_res"])

            string_res = create_string(results_complete)
            string_res_total.append(string_res)

            # ncd
            ncd_full.append(results_dict["ncd"])

            len_repertoire.append(repertoire_length)
            ngen.append(results_dict["parameters"]["generations"])
            tmin.append(results_dict["parameters"]["t_min "])
            fit_thres_ful.append(results_dict["parameters"]["fitness_threshold"])
            diss_thres_ful.append(results_dict["parameters"]["dissim_threshold"])
            crit_1_total.append(crit1)
            min_typ.append(average(calculate_typicality_with_min_distance_from_files(
                results=results_complete, repertoire=repertoire)))
            crit_2_total.append(crit2)
            print path
            index1.append(path.split("\\")[1])
            index2.append(path.split("\\")[2])
            # archive
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
                sbc_archive.append(results_dict["sbc_arch"])

                for x in results_complete_archive.values():
                    results_archive.append(["choreo"])
                    archive_string_complete = archive_string_complete + "".join(x["choreo"])
                    avg_fit_archive = avg_fit_archive + x["fitness"]
                    fitness_Arch.append(x["fitness"])
                    ncd_local.append(compute_ncd("".join(x["choreo"]), string_rep))
                    nov_local.append(x["dissim"])

                all_results["archive"] = fitness_Arch
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

            # sbc for random
            sbc = SBC("bz2", "9", sbc_rnd)
            sbc_res.append(sbc.compute())
            sbc_rep.append("")
            sbc_archive.append("")

            index2.append("random")
            ncd_full.append(compute_ncd(rand_ind, string_rep))
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
            crit_1_total.append(crit_1_rand)
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
    '01 parameters': index1,
    "02 method": index2,
    "03 ncd": ncd_full,
    "04 sbc_res": sbc_res,
    '05 criterion 1': crit_1_total,
    '06 average min_typicality': min_typ,
    "07 avg_fit": avg_fit_total,
    "08 avg_novelty": avg_nov_total,
    "09 sbc_rep": sbc_rep,
    "10 sbc_archive": sbc_archive,
    '11 criterion 2 with ncd': crit_2_total,
    "12 len_Arch": len_Arch_full,
    "13 full ncd archive": full_ncd_archive_total,
    "14 criterion 1 archive": criterion1_archive_total,
    "15 fitness archive average": fitness_archive_total,
    "16 criterion 2 archive": criterion2_archive_total,
    "17 average min typicality archive": average_min_typicality_archive_total,
    "18 gen_fitness": gen_fitness_total,
    "19 fit thresh": fit_thres_ful,
    "20 diss thresh": diss_thres_ful,
    "21 ngen": ngen,
    "22 tmin": tmin,
    "23 lenrep": len_repertoire,
    "24 len_res": len_res_full,
    "25 string_res": string_res_total,
})
df.to_excel("../data/results/" + filename + ".xlsx", sheet_name='sheet1', index=False)

print "evaluation ended"

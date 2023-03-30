import pandas as pd

oai = pd.read_csv('data_KL_samples.csv')
pts5= pd.read_csv('data_patients.csv')

kl_avg = pd.DataFrame()
for lr in ["Left","Right"]:
    for kl in [0,1,2,3,4]:
    # for j in ["side","inner","mid"]:

        res= oai[(oai["kl"]==kl) & (oai["side"]==lr)].mean()
        print(res)
        res= res.to_dict()
        res["side"]=lr
        kl_avg = kl_avg.append(res,ignore_index=True)
            # {'fileLocation': image, 'file_name': file_name, 'side': side, 'inner': areas[0], 'mid': areas[1],
            #             'outer': areas[2], "kl": kl},
            #            ignore_index=True)

kl_avg.to_csv('.\\data_KL_average.csv', index=False)

kl_asg = pd.DataFrame()
for patinet in ["Patient 1","Patient 2","Patient 3","Patient 4","Patient 5"]:
    for lr in ["Left", "Right"]:
        for j in ["outer", "inner", "mid"]:

            res_pts = pts5[(pts5["color"] == patinet) & (pts5["side"] == lr)][j]
            res_dic={}
            for kl in [0,1,2,3,4]:
                res_kl = kl_avg[(kl_avg["kl"] == kl) & (kl_avg["side"] == lr)][j]
                # print("res_pts:",res_pts)
                # print("res_kl:",  res_kl)
                # exit()
                res_dic[kl]= abs(float(res_pts)-float(res_kl))

            kl_assigned=min(res_dic, key=res_dic.get)
            kl_asg = kl_asg.append( {'kl': kl_assigned, 'lr': lr,'side':j,"Patient":patinet}, ignore_index=True)
            # {'fileLocation': image, 'file_name': file_name, 'side': side, 'inner': areas[0], 'mid': areas[1],
            #             'outer': areas[2], "kl": kl},
            #            ignore_index=True)
kl_asg.to_csv('.\\data_KL_assgined.csv', index=False)

# for patinet in ["Patient 1","Patient 2","Patient 3","Patient 4","Patient 5"]:
#     for lr in ["Left", "Right"]:
#         for j in ["outer", "inner", "mid"]:
#          = kl_avg[(kl_avg["kl"] == kl) & (kl_avg["side"] == lr)][j]
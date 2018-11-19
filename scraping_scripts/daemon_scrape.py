# from subprocess import call
from subprocess import Popen

categories_dict = {"windows": ["start","hardware","desktop","ecoms","files","gaming","windows_install","pictures","networking","winapps","performance","windows_programs","tms","security","update"],
                    "msoffice": ["msoffice_install","msoffice_account","msoffice_o365Admin","msoffice_officeinsider","msoffice_delve","msoffice_access", "msoffice_excel","msoffice_forms","msoffice_infop","msoffice_onenote","msoffice_outlook","msoffice_powerpoint","msoffice_project","msoffice_publish","msoffice_sharepoint","msoffice_sway","msoffice_todo","msoffice_trans","msoffice_visio","msoffice_word","msoffice_yammer","msoffice_drive","msoffice_onedrivefb","msoffice_otherapps","msoffice_sfb","msoffice_other"],
                    "xbox": ["xba_acc","xba_gapp","xba_neteq","xba_sapro","xba_tveq","xba_console","xba_modi","xba_wowpc"],
                    "outlook_com": ["oemail","opeople","oaccount","osecurity","omessaging","ocalendar","osettings","opersonalization"],
                    "skype": ["sk_sign","sk_call","sk_mess","sk_con","sk_acc","sk_pay","sk_priv","sk_bot","sk_access","sk_else","sk_in","sk_dev","sk_news"],
                    "surface": ["surfheadph","surfgo","surflap2","surflaptop","surfpro6","surfpronew","surfpro4","surfpro3","surfpro2","surfpro","surfstudio2","surfstudio","surfbook2","surfbook","surf3","surf2","surfwinrt","surfaccesso"],
                    "insider": ["insider_wintp","insider_internet","insider_office","insider_apps","insider_prog","insider_games","insider_cortanapreview"],
                    "edge": ["edge_open","edge_video","edge_history","edge_search","edge_crash","edge_speed","edge_read","edge_extension","edge_issue","edge_other"],
                    "protect": ["mse","protect_scanner","protect_defender","defender_offline","protect_other"],
                    "ie": ["ie11","ie10","ie9","ie8","ie7_6","ie_other"],
                    "bing": ["bing_gettingstarted","bing_websearch","bing_mobile","bing_map","bing_apps","bing_safety","bing_ads","bing_other"],
                    "musicandvideo": ["xboxmusic","xboxvideo","winmediaplayer","xbmusic","xbvideo","xbzune"],
                    "newmsn": ["newmsn_signup","newmsn_set","newmsn_browse","newmsn_install","newmsn_explorer"],
                    "band": ["msband","msband2"],
                    "education_ms": ["edu_office","edu_win10","edu_surface","edu_onenote","edu_onclass","edu_onstaff","edu_learntool","edu_msteams","edu_msclass","edu_forms","edu_sway"],
                    "windowslive": ["messenger","gallery","moviemaker","livemail","writer"],
                    "mobiledevices": ["mdlumia","mdwindows","mdasha","mdnokian","mdaccessories"]
                    }
process_pool = []
for main_cat in categories_dict:
    for sub_cat in categories_dict[main_cat]:
        print("{} {}".format(main_cat,sub_cat))
        process_pool.append(Popen("py retrograde_scrape.py {} {} 1 11 5 2017".format(main_cat,sub_cat)))
    while len(process_pool) != 0:
        for index, proc in enumerate(process_pool):
            if proc.poll() is not None:
                arg_tokens = proc.args.split()
                print("finished running {} {}".format(arg_tokens[2],arg_tokens[3]))
                del process_pool[index]
                file_name = "MS_Answers_{}_{}.txt".format(arg_tokens[2],arg_tokens[3])
                Popen("py process_individual_file.py {}".format(file_name))

#Save files format "MS_Answers_{}_{}.txt".format(main_category,sub_category)

# while len(process_pool) != 0:
#     for index, proc in enumerate(process_pool):
#         if proc.poll() is not None:
#             arg_tokens = proc.args.split()
#             print("finished running {} {}".format(arg_tokens[2],arg_tokens[3]))
#             del process_pool[index]
#             file_name = "MS_Answers_{}_{}.txt".format(arg_tokens[2],arg_tokens[3])
#             Popen("py process_individual_file.py {}".format(file_name))

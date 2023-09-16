from visualise import visualise 
import pandas as pd
import json

# visualise.plotAll()

# import snaction data 
# with open("../Tracking Visualisations/final tests/Fixed 10 Rounds/output/survivorsTrack10F.json") as json_data:
#             data = json.load(json_data)
#             survivors1 = pd.DataFrame(data)
# # print(survivors1)
# with open("../Tracking Visualisations/final tests/Predict 10 Rounds/output/survivorsTrack10P.json") as json_data:
#             data = json.load(json_data)
#             survivors2 = pd.DataFrame(data)
# with open("../Tracking Visualisations/final tests/Random 10 Rounds/output/survivorsTrack10R.json") as json_data:
#             data = json.load(json_data)
#             survivors3 = pd.DataFrame(data)
# df1 = pd.read_csv("../Training Visualisation/final tests/Fixed 10 Rounds/output/survivorsTrack10F.csv")
# df2 = pd.read_csv("../Training Visualisation/final tests/Predict 10 Rounds/output/survivorsTrack10P.csv")
# df3 = pd.read_csv("../Training Visualisation/final tests/Random 10 Rounds/output/survivorsTrack10R.csv")

# plot shit
# visualise.plot_track(survivors1, "survivors10F.png")
# visualise.plot_track(survivors2, "survivorsP10.png")
# visualise.plot_track(survivors3, "survivors10R.png")
with open("survivorsTrackEDIT.json") as json_data:
            data = json.load(json_data)
            survivors4 = pd.DataFrame(data)


visualise.plot_sanctioned(survivors4, "sanctionedP10")


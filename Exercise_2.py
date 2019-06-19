{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 35
    },
    "colab_type": "code",
    "id": "hXyK9eRrVuHL",
    "outputId": "5467a202-607e-4e67-d910-731695f5b038"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Drive already mounted at /content/gdrive; to attempt to forcibly remount, call drive.mount(\"/content/gdrive\", force_remount=True).\n"
     ]
    }
   ],
   "source": [
    "from google.colab import drive\n",
    "\n",
    "drive.mount(\"/content/gdrive\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 35
    },
    "colab_type": "code",
    "id": "lzUxnhNvV6AU",
    "outputId": "e9145d66-c2b8-4dac-9177-877171276f92"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "/content/gdrive/My Drive/SAKI/Exercise_2\n"
     ]
    }
   ],
   "source": [
    "cd /content/gdrive/My Drive/SAKI/Exercise_2"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 0,
   "metadata": {
    "colab": {},
    "colab_type": "code",
    "id": "mB80Yy0XVcRS"
   },
   "outputs": [],
   "source": [
    "import os\n",
    "import json\n",
    "dataset_path = \"DataSet.json\"\n",
    "#print(\"Path exists? {}\".format(os.path.exists(dataset_path)))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 0,
   "metadata": {
    "colab": {},
    "colab_type": "code",
    "id": "fp03KGxsV_65"
   },
   "outputs": [],
   "source": [
    "## use the \"open\" function to get a filehandle. \n",
    "with open(dataset_path,encoding=\"utf8\") as f:\n",
    "    doc = f.readlines()\n",
    "    \n",
    "all_resumes = []\n",
    "for line in doc:\n",
    "    all_resumes.append(json.loads(line))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 35
    },
    "colab_type": "code",
    "id": "jpcQTQiNWX86",
    "outputId": "23e7996c-88ae-4abe-e5fa-ba36c58502dc"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "690\n"
     ]
    }
   ],
   "source": [
    "## data conversion method\n",
    "def convert_data(data):\n",
    "    \"\"\"\n",
    "    Creates NER training data in Spacy format from JSON dataset\n",
    "    Outputs the Spacy training data which can be used for Spacy training.\n",
    "    \"\"\"\n",
    "    text = data['content']\n",
    "    entities = []\n",
    "    if data['annotation'] is not None:\n",
    "        for annotation in data['annotation']:\n",
    "            # only a single point in text annotation.\n",
    "            point = annotation['points'][0]\n",
    "            labels = annotation['label']\n",
    "            # handle both list of labels or a single label.\n",
    "            if not isinstance(labels, list):\n",
    "                labels = [labels]\n",
    "            for label in labels:\n",
    "                # dataturks indices are both inclusive [start, end] but spacy is not [start, end)\n",
    "                entities.append((point['start'], point['end'] + 1, label))\n",
    "    # become list of Content string, \"entities\" start end \"label\", start end \"label\"...\n",
    "    # maybe clean empty rows?\n",
    "    return (text, {\"entities\": entities})\n",
    "   \n",
    "## TODO using a loop or list comprehension, convert each resume \n",
    "#in all_resumes using the convert function above, storing the result\n",
    "converted_resumes = []\n",
    "converted_resumes = [convert_data(line) for line in all_resumes]\n",
    "\n",
    "# filter out resumes where resume entities list is None\n",
    "\n",
    "converted_resumes = [line for line in converted_resumes if len(line[1][\"entities\"]) > 0]\n",
    "print(len(converted_resumes))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 74
    },
    "colab_type": "code",
    "id": "LRLuskYxWrkr",
    "outputId": "fc611673-562e-41e4-abbe-2062a908a004"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Entity labels:  {'Location', 'College', 'projects', 'Certifications', 'UNKNOWN', 'Years of Experience', 'Rewards and Achievements', 'Graduation Year', 'Name', 'University', 'links', 'Designation', 'state', 'College Name', 'Relocate to', 'abc', 'des', 'Links', 'Companies worked at', 'Email Address', 'training', 'Can Relocate to', 'Skills', 'Address', 'Degree'}\n",
      "25\n"
     ]
    }
   ],
   "source": [
    "## collect names of all entities in complete resume dataset\n",
    "all_labels = list()\n",
    "for res in converted_resumes:\n",
    "    ## entity list of res\n",
    "    for ents in res[1]['entities']:\n",
    "        all_labels.append(ents[2])  \n",
    "        \n",
    "# Make labels a set of unique values\n",
    "unique_labels = set(all_labels)\n",
    "## Print unique entity labels\n",
    "print(\"Entity labels: \",unique_labels)\n",
    "print(len(unique_labels))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 0,
   "metadata": {
    "colab": {},
    "colab_type": "code",
    "id": "N--2VPGUXDCA"
   },
   "outputs": [],
   "source": [
    "#Create File as reference\n",
    "converted_resumes_path = r\"C:\\Users\\matth\\Documents\\Uni\\Master\\Kurse\\SAKI\\Exercise_2_fin.json\"\n",
    "with open(converted_resumes_path,\"w\", encoding = \"UTF-8\") as file_write:\n",
    "    json.dump(converted_resumes,file_write)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "colab_type": "text",
    "id": "WnUGNaFNXhVB"
   },
   "source": [
    "Preprocessing of Data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 0,
   "metadata": {
    "colab": {},
    "colab_type": "code",
    "id": "qPnGti2NXaFa"
   },
   "outputs": [],
   "source": [
    "import spacy\n",
    "from spacy_train_resume_ner import train_spacy_ner\n",
    "path = r\"Exercise_2_fin.json\"\n",
    "with open(path) as json_file:\n",
    "    resumes = json.load(json_file)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 146
    },
    "colab_type": "code",
    "id": "jGEsaPmpW16a",
    "outputId": "5fe64528-3725-4a27-e384-20b01cf6f464"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Docs with Degree: 606\n",
      "Total count of Degree: 1012\n",
      "Docs with Designation: 650\n",
      "Total count of Designation: 2842\n",
      "Docs with Companies worked at: 627\n",
      "Total count of Companies worked at: 2830\n",
      "Gathered 547 training examples\n"
     ]
    }
   ],
   "source": [
    "## Entities for training:\n",
    "chosen_entity_labels = [\"Degree\", \"Designation\",\"Companies worked at\"]\n",
    "\n",
    "## check if the chosen entities are sufficient\n",
    "for chosen in chosen_entity_labels:\n",
    "    found_docs_with_entity = 0\n",
    "    entity_count = 0\n",
    "    for resume in converted_resumes:\n",
    "        entity_list = resume[1][\"entities\"]\n",
    "        _,_,labels = zip(*entity_list)\n",
    "        if chosen in labels:\n",
    "            found_docs_with_entity+=1\n",
    "            entity_count+=len([l for l in labels if l == chosen])\n",
    "    print(\"Docs with {}: {}\".format(chosen,found_docs_with_entity))\n",
    "    print(\"Total count of {}: {}\".format(chosen,entity_count))\n",
    "\n",
    "#gathers all resumes which have all of the chosen entites above.\n",
    "def gather_candidates(dataset,entity_labels):\n",
    "    candidates = list()\n",
    "    for resume in dataset:\n",
    "        res_ent_labels = list(zip(*resume[1][\"entities\"]))[2]\n",
    "        if set(entity_labels).issubset(res_ent_labels):\n",
    "            candidates.append(resume)\n",
    "    return candidates\n",
    "#store gathered resumes for training\n",
    "training_data = gather_candidates(resumes, chosen_entity_labels)\n",
    "print(\"Gathered {} training examples\".format(len(training_data)))\n",
    "#print(training_data)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 185
    },
    "colab_type": "code",
    "id": "3uP8iWZvYck7",
    "outputId": "5a3be40d-71d8-45d3-fce1-157df6e3e985"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Created blank 'en' model\n",
      "Exception thrown when processing doc:\n",
      "('Nida Khan\\nTech Support Executive - Teleperformance for Microsoft\\n\\nJaipur, Rajasthan - Email me on Indeed: indeed.com/r/Nida-Khan/6c9160696f57efd8\\n\\n• To be an integral part of the organization and enhance my knowledge to utilize it in a productive\\nmanner for the growth of the company and the global.\\n\\nINDUSTRIAL TRAINING\\n\\n• BHEL, (HEEP) HARIDWAR\\nOn CNC System&amp; PLC Programming.\\n\\nWORK EXPERIENCE\\n\\nTech Support Executive\\n\\nTeleperformance for Microsoft -\\n\\nSeptember 2017 to Present\\n\\nprocess.\\n• 21 months of experience in ADFC as Phone Banker.\\n\\nEDUCATION\\n\\nBachelor of Technology in Electronics & communication Engg\\n\\nGNIT institute of Technology -  Lucknow, Uttar Pradesh\\n\\n2008 to 2012\\n\\nClass XII\\n\\nU.P. Board -  Bareilly, Uttar Pradesh\\n\\n2007\\n\\nClass X\\n\\nU.P. Board -  Bareilly, Uttar Pradesh\\n\\n2005\\n\\nSKILLS\\n\\nMicrosoft office, excel, cisco, c language, cbs. (4 years)\\n\\nhttps://www.indeed.com/r/Nida-Khan/6c9160696f57efd8?isid=rex-download&ikw=download-top&co=IN',) ({'entities': [[552, 610, 'Degree'], [420, 449, 'Companies worked at'], [395, 418, 'Designation'], [35, 64, 'Companies worked at'], [10, 33, 'Designation'], [9, 32, 'Designation']]},)\n",
      "Losses {'ner': 48460.13242870225}\n",
      "Unfiltered training data size:  547\n",
      "Filtered training data size:  546\n",
      "Bad data size:  1\n",
      "amount of resumes used: 546\n"
     ]
    }
   ],
   "source": [
    "## filter all annotation based on filter list\n",
    "def filter_ents(ents, filter):\n",
    "    filtered = [ent for ent in ents if ent[2] in filter]\n",
    "    return filtered\n",
    "\n",
    "X = [filter_ents(line[1][\"entities\"],chosen_entity_labels) for line in training_data]\n",
    "for i in range(0,len(training_data)):\n",
    "    training_data[i][1][\"entities\"]=X[i]\n",
    "    \n",
    "#remove additional bad data    \n",
    "def remove_bad_data(training_data):\n",
    "    model, baddocs = train_spacy_ner(training_data, debug=True, n_iter=1)\n",
    "    filtered = [data for data in training_data if data[0] not in baddocs]\n",
    "    print(\"Unfiltered training data size: \",len(training_data))\n",
    "    print(\"Filtered training data size: \", len(filtered))\n",
    "    print(\"Bad data size: \", len(baddocs))\n",
    "    return filtered\n",
    "\n",
    "## call remove method \n",
    "X = remove_bad_data(training_data)\n",
    "\n",
    "print(\"amount of resumes used:\", len(X))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "colab_type": "text",
    "id": "MYC0jweqZq39"
   },
   "source": [
    "Train Test Split"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 0,
   "metadata": {
    "colab": {},
    "colab_type": "code",
    "id": "CkYa1bQ2YyHm"
   },
   "outputs": [],
   "source": [
    "import math\n",
    "\n",
    "def train_test_split(X,train_percent):\n",
    "    train_size = math.ceil(train_percent*len(X))\n",
    "    train = X[:train_size]\n",
    "    test = X[train_size:len(X)]\n",
    "    assert len(train) + len(test) == len(X)\n",
    "    return train,test\n",
    "\n",
    "#  storing results in \"train\" and \"test\" variables.\n",
    "train,test = train_test_split(X,0.8)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "colab_type": "text",
    "id": "PhR-i_vYZ7G5"
   },
   "source": [
    "Training with spacy:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 498
    },
    "colab_type": "code",
    "id": "LbS-PtbOXeEU",
    "outputId": "68114386-83e3-4f7e-e481-c6162fd09dda"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Created blank 'en' model\n",
      "Losses {'ner': 31968.13767113188}\n",
      "Losses {'ner': 30228.88540965278}\n",
      "Losses {'ner': 32919.31922331465}\n",
      "Losses {'ner': 29931.20157718868}\n",
      "Losses {'ner': 22511.304856944986}\n",
      "Losses {'ner': 16026.407853444325}\n",
      "Losses {'ner': 15265.29558838547}\n",
      "Losses {'ner': 9321.272257674671}\n",
      "Losses {'ner': 7936.275811117183}\n",
      "Losses {'ner': 7390.836710034936}\n",
      "Losses {'ner': 6677.588832632146}\n",
      "Losses {'ner': 6137.447280326258}\n",
      "Losses {'ner': 5651.897764431078}\n",
      "Losses {'ner': 5461.901170262701}\n",
      "Losses {'ner': 5242.662501492144}\n",
      "Losses {'ner': 5569.673595578974}\n",
      "Losses {'ner': 5138.93379673189}\n",
      "Losses {'ner': 4824.357937028413}\n",
      "Losses {'ner': 5164.173623887769}\n",
      "Losses {'ner': 5191.560264433296}\n",
      "Losses {'ner': 4566.599843960386}\n",
      "Losses {'ner': 4079.5635391785554}\n",
      "Losses {'ner': 4858.4511767389795}\n",
      "Losses {'ner': 4148.24659953339}\n",
      "Losses {'ner': 3950.447255169211}\n"
     ]
    }
   ],
   "source": [
    "custom_nlp,_= train_spacy_ner(train,n_iter=25)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "colab_type": "text",
    "id": "YMLh8t6napuj"
   },
   "source": [
    "Formatting data into iob format"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 0,
   "metadata": {
    "colab": {},
    "colab_type": "code",
    "id": "AMVkEswianW8"
   },
   "outputs": [],
   "source": [
    "from spacy.gold import biluo_tags_from_offsets\n",
    "import pandas as pd\n",
    "from IPython.display import display, HTML\n",
    "\n",
    "## returns a pandas dataframe with tokens, prediction, and true (Gold Standard) annotations of tokens\n",
    "def make_bilou_df(nlp,resume):\n",
    "    \"\"\"\n",
    "    param nlp - a trained spacy model\n",
    "    param resume - a resume from our train or test set\n",
    "    \"\"\"\n",
    "    doc = nlp(resume[0])\n",
    "    bilou_ents_predicted = biluo_tags_from_offsets(doc, [(ent.start_char,ent.end_char,ent.label_)for ent in doc.ents])\n",
    "    bilou_ents_true = biluo_tags_from_offsets(doc,\n",
    "                                                   [(ent[0], ent[1], ent[2]) for ent in resume[1][\"entities\"]])\n",
    "    \n",
    "    doc_tokens = [tok.text for tok in doc]\n",
    "    bilou_df = pd.DataFrame()\n",
    "    bilou_df[\"Tokens\"] =doc_tokens\n",
    "    bilou_df[\"Tokens\"] = bilou_df[\"Tokens\"].str.replace(\"\\\\s+\",\"\") \n",
    "    #bilou_df[\"Predicted\"] = bilou_ents_predicted\n",
    "    bilou_df[\"Predicted\"] = bilou_ents_predicted\n",
    "    bilou_df[\"True\"] = bilou_ents_true\n",
    "    #transform bilou format into iob format\n",
    "    bilou_df[\"True\"].replace(to_replace =\"L-\",value= \"I-\",regex=True, inplace=True)\n",
    "    bilou_df[\"Predicted\"].replace(to_replace =\"L-\",value= \"I-\",regex=True, inplace=True)\n",
    "    bilou_df[\"True\"].replace(to_replace =\"U-\",value= \"I-\",regex=True, inplace=True)\n",
    "    bilou_df[\"Predicted\"].replace(to_replace =\"U-\",value= \"I-\",regex=True, inplace=True)\n",
    "    bilou_df[\"Predicted\"].replace(to_replace =\" \",value= \"_\",regex=True, inplace=True)\n",
    "    bilou_df[\"True\"].replace(to_replace =\" \",value= \"_\",regex=True, inplace=True)\n",
    "    return bilou_df \n",
    "    \n",
    "## store a resume from test set\n",
    "bilou_df = make_bilou_df(custom_nlp,resume)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "colab_type": "text",
    "id": "x31UvkLrjTat"
   },
   "source": [
    "Evaluation of SpaCy model"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 458
    },
    "colab_type": "code",
    "id": "2kiA0U9SjRDw",
    "outputId": "06e3d444-cebe-4d34-b206-37c247edabbd"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Accuracy:  0.9657573570458512\n",
      "For label 'Degree' tp: 415 fp: 330 fn: 59\n",
      "Precision:  0.5570469798657718\n",
      "Recall:  0.8755274261603375\n",
      "F1:  0.6808859721082854\n",
      "For label 'Designation' tp: 834 fp: 418 fn: 269\n",
      "Precision:  0.6661341853035144\n",
      "Recall:  0.7561196736174071\n",
      "F1:  0.7082802547770701\n",
      "For label 'Companies_worked_at' tp: 925 fp: 400 fn: 345\n",
      "Precision:  0.6981132075471698\n",
      "Recall:  0.7283464566929134\n",
      "F1:  0.7129094412331405\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>precision</th>\n",
       "      <th>recall</th>\n",
       "      <th>f1</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>Degree</th>\n",
       "      <td>0.557047</td>\n",
       "      <td>0.875527</td>\n",
       "      <td>0.680886</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Designation</th>\n",
       "      <td>0.666134</td>\n",
       "      <td>0.756120</td>\n",
       "      <td>0.708280</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Companies_worked_at</th>\n",
       "      <td>0.698113</td>\n",
       "      <td>0.728346</td>\n",
       "      <td>0.712909</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                     precision    recall        f1\n",
       "Degree                0.557047  0.875527  0.680886\n",
       "Designation           0.666134  0.756120  0.708280\n",
       "Companies_worked_at   0.698113  0.728346  0.712909"
      ]
     },
     "metadata": {
      "tags": []
     },
     "output_type": "display_data"
    },
    {
     "data": {
      "text/plain": [
       "precision    0.640431\n",
       "recall       0.786665\n",
       "f1           0.700692\n",
       "dtype: float64"
      ]
     },
     "metadata": {
      "tags": []
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "import numpy as np\n",
    "doc_accuracy = []\n",
    "chosen_entity_labels = [\"Degree\", \"Designation\",\"Companies_worked_at\"]\n",
    "#calculate accuracy\n",
    "for res in test:\n",
    "    ## for each 'res' \n",
    "    bilou_df = make_bilou_df(custom_nlp,res)\n",
    "    same_df = bilou_df[bilou_df[\"Predicted\"] == bilou_df[\"True\"]]\n",
    "    accuracy = len(same_df)/len(bilou_df)\n",
    "    doc_accuracy.append(accuracy)\n",
    "# average accuracy\n",
    "total_acc = np.average(doc_accuracy)\n",
    "print(\"Accuracy: \",total_acc)\n",
    "\n",
    "#calculating scores for each entity\n",
    "data = []\n",
    "for label in chosen_entity_labels:\n",
    "    ## variables to store results for all resumes for one entity type\n",
    "    true_positives = 0\n",
    "    false_positives = 0\n",
    "    false_negatives = 0\n",
    "\n",
    "    for tres in test:        \n",
    "        tres_df = make_bilou_df(custom_nlp,tres)\n",
    "               \n",
    "        ## calculate true false positives and false negatives for each resume\n",
    "        tp = tres_df[(tres_df[\"Predicted\"]== tres_df[\"True\"]) & (tres_df[\"Predicted\"].str.contains(label))]\n",
    "        fp = tres_df[(tres_df[\"Predicted\"] != tres_df[\"True\"]) & (tres_df[\"Predicted\"].str.contains(label))]\n",
    "        fn = tres_df[(tres_df[\"Predicted\"] != tres_df[\"True\"]) & (tres_df[\"True\"].str.contains(label))]\n",
    "        ## aggregate result for each resume to totals\n",
    "        true_positives += tp.shape[0]\n",
    "        false_positives += fp.shape[0]\n",
    "        false_negatives += fn.shape[0]\n",
    "\n",
    "    print(\"For label '{}' tp: {} fp: {} fn: {}\".format(label,true_positives,false_positives,false_negatives))\n",
    "    \n",
    "    precision = true_positives /(true_positives + false_positives)\n",
    "    recall = true_positives / (true_positives + false_negatives)\n",
    "    f1 = 2*((precision * recall) / (precision + recall))\n",
    "    print(\"Precision: \",precision)\n",
    "    print(\"Recall: \",recall)\n",
    "    print(\"F1: \",f1)\n",
    "    row = [precision,recall,f1]\n",
    "    data.append(row)\n",
    "\n",
    "## pandas dataframe with metrics data.\n",
    "metric_df = pd.DataFrame(data, index = chosen_entity_labels,columns =[\"precision\",\"recall\",\"f1\"] )\n",
    "display(metric_df)\n",
    "\n",
    "## Averaged metrics\n",
    "avg_metr = pd.DataFrame.mean(metric_df)\n",
    "display(avg_metr)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "colab_type": "text",
    "id": "B0FqXmBykFAK"
   },
   "source": [
    "Create files and remove inconsistencies"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 0,
   "metadata": {
    "colab": {},
    "colab_type": "code",
    "id": "bG-2JDkskDTy"
   },
   "outputs": [],
   "source": [
    "## TODO persist IOB data as text\n",
    "import re\n",
    "print(\"Make bilou dfs\")\n",
    "training_data_as_bilou = [make_bilou_df(custom_nlp,res) for res in train]\n",
    "test_data_as_bilou = [make_bilou_df(custom_nlp,res) for res in test]\n",
    "\n",
    "\n",
    "print(\"Done!\")\n",
    "training_df = pd.DataFrame(columns = [\"text\",\"ner\",\"doc\",\"ner_spacy\"])\n",
    "test_df = pd.DataFrame(columns = [\"text\",\"ner\",\"doc\",\"ner_spacy\"])\n",
    "for idx,df in enumerate(training_data_as_bilou):\n",
    "    df2 = pd.DataFrame()\n",
    "    df2[\"text\"] = df[\"Tokens\"]\n",
    "    df2[\"ner\"] = df[\"True\"]\n",
    "    df2[\"ner_spacy\"] = df[\"Predicted\"]\n",
    "    df2[\"doc\"] = idx\n",
    "    training_df = training_df.append(df2)\n",
    "\n",
    "training_df=training_df[training_df[\"ner\"]!=\"-\"]\n",
    "\n",
    "#Sentence seperator\n",
    "training_df.loc[(training_df[\"text\"]==\"\"),'ner_spacy']=\"\"\n",
    "training_df.loc[(training_df[\"text\"]==\"\"),'ner']=\"\"\n",
    "training_df.loc[(training_df[\"text\"]==\"\"),'doc']=\"\"\n",
    "\n",
    "\n",
    "for idx,df in enumerate(test_data_as_bilou):\n",
    "     df2 = pd.DataFrame()\n",
    "     df2[\"text\"] = df[\"Tokens\"]\n",
    "     df2[\"ner\"] = df[\"True\"]\n",
    "     df2[\"ner_spacy\"] = df[\"Predicted\"]\n",
    "     df2[\"doc\"] = idx\n",
    "     test_df = test_df.append(df2)\n",
    "      \n",
    "test_df=test_df[test_df[\"ner\"]!=\"-\"]\n",
    "\n",
    "#Sentence seperator\n",
    "test_df.loc[(test_df[\"text\"]==\"\"),'ner_spacy']=\"\"\n",
    "test_df.loc[(test_df[\"text\"]==\"\"),'ner']=\"\"\n",
    "test_df.loc[(test_df[\"text\"]==\"\"),'doc']=\"\"\n",
    "\n",
    "\n",
    "\n",
    "with open(\"train_res_bilou.txt\",'w+',encoding = \"utf-8\") as f:\n",
    "  training_df.to_csv(f,sep = \" \",encoding = \"utf-8\",index = False, header =False)\n",
    "  \n",
    "with open(\"test_res_bilou.txt\",'w+',encoding = \"utf-8\") as f:\n",
    "  test_df.to_csv(f,sep = \" \",encoding = \"utf-8\",index = False,header = False)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "colab_type": "text",
    "id": "eFHg4foD9Fgo"
   },
   "source": [
    "Flair model"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 1423
    },
    "colab_type": "code",
    "id": "C8P9gXSHeexH",
    "outputId": "c15ea8ec-0c8a-44d3-c93a-36c7bdf9b4e2"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Collecting flair\n",
      "\u001b[?25l  Downloading https://files.pythonhosted.org/packages/4e/3a/2e777f65a71c1eaa259df44c44e39d7071ba8c7780a1564316a38bf86449/flair-0.4.2-py3-none-any.whl (136kB)\n",
      "\u001b[K     |████████████████████████████████| 143kB 2.9MB/s \n",
      "\u001b[?25hCollecting segtok>=1.5.7 (from flair)\n",
      "  Downloading https://files.pythonhosted.org/packages/1d/59/6ed78856ab99d2da04084b59e7da797972baa0efecb71546b16d48e49d9b/segtok-1.5.7.tar.gz\n",
      "Collecting deprecated>=1.2.4 (from flair)\n",
      "  Downloading https://files.pythonhosted.org/packages/9f/7a/003fa432f1e45625626549726c2fbb7a29baa764e9d1fdb2323a5d779f8a/Deprecated-1.2.5-py2.py3-none-any.whl\n",
      "Requirement already satisfied: urllib3<1.25,>=1.20 in /usr/local/lib/python3.6/dist-packages (from flair) (1.24.3)\n",
      "Collecting mpld3==0.3 (from flair)\n",
      "\u001b[?25l  Downloading https://files.pythonhosted.org/packages/91/95/a52d3a83d0a29ba0d6898f6727e9858fe7a43f6c2ce81a5fe7e05f0f4912/mpld3-0.3.tar.gz (788kB)\n",
      "\u001b[K     |████████████████████████████████| 798kB 41.7MB/s \n",
      "\u001b[?25hRequirement already satisfied: tabulate in /usr/local/lib/python3.6/dist-packages (from flair) (0.8.3)\n",
      "Collecting regex (from flair)\n",
      "\u001b[?25l  Downloading https://files.pythonhosted.org/packages/6f/4e/1b178c38c9a1a184288f72065a65ca01f3154df43c6ad898624149b8b4e0/regex-2019.06.08.tar.gz (651kB)\n",
      "\u001b[K     |████████████████████████████████| 655kB 44.2MB/s \n",
      "\u001b[?25hRequirement already satisfied: torch>=1.0.0 in /usr/local/lib/python3.6/dist-packages (from flair) (1.1.0)\n",
      "Requirement already satisfied: tqdm>=4.26.0 in /usr/local/lib/python3.6/dist-packages (from flair) (4.28.1)\n",
      "Requirement already satisfied: sklearn in /usr/local/lib/python3.6/dist-packages (from flair) (0.0)\n",
      "Requirement already satisfied: hyperopt>=0.1.1 in /usr/local/lib/python3.6/dist-packages (from flair) (0.1.2)\n",
      "Collecting pytorch-pretrained-bert>=0.6.1 (from flair)\n",
      "\u001b[?25l  Downloading https://files.pythonhosted.org/packages/d7/e0/c08d5553b89973d9a240605b9c12404bcf8227590de62bae27acbcfe076b/pytorch_pretrained_bert-0.6.2-py3-none-any.whl (123kB)\n",
      "\u001b[K     |████████████████████████████████| 133kB 40.3MB/s \n",
      "\u001b[?25hCollecting bpemb>=0.2.9 (from flair)\n",
      "  Downloading https://files.pythonhosted.org/packages/bc/70/468a9652095b370f797ed37ff77e742b11565c6fd79eaeca5f2e50b164a7/bpemb-0.3.0-py3-none-any.whl\n",
      "Requirement already satisfied: pytest>=3.6.4 in /usr/local/lib/python3.6/dist-packages (from flair) (3.6.4)\n",
      "Collecting sqlitedict>=1.6.0 (from flair)\n",
      "  Downloading https://files.pythonhosted.org/packages/0f/1c/c757b93147a219cf1e25cef7e1ad9b595b7f802159493c45ce116521caff/sqlitedict-1.6.0.tar.gz\n",
      "Requirement already satisfied: gensim>=3.4.0 in /usr/local/lib/python3.6/dist-packages (from flair) (3.6.0)\n",
      "Requirement already satisfied: matplotlib>=2.2.3 in /usr/local/lib/python3.6/dist-packages (from flair) (3.0.3)\n",
      "Requirement already satisfied: wrapt<2,>=1 in /usr/local/lib/python3.6/dist-packages (from deprecated>=1.2.4->flair) (1.11.1)\n",
      "Requirement already satisfied: numpy in /usr/local/lib/python3.6/dist-packages (from torch>=1.0.0->flair) (1.16.4)\n",
      "Requirement already satisfied: scikit-learn in /usr/local/lib/python3.6/dist-packages (from sklearn->flair) (0.21.2)\n",
      "Requirement already satisfied: networkx in /usr/local/lib/python3.6/dist-packages (from hyperopt>=0.1.1->flair) (2.3)\n",
      "Requirement already satisfied: pymongo in /usr/local/lib/python3.6/dist-packages (from hyperopt>=0.1.1->flair) (3.8.0)\n",
      "Requirement already satisfied: six in /usr/local/lib/python3.6/dist-packages (from hyperopt>=0.1.1->flair) (1.12.0)\n",
      "Requirement already satisfied: future in /usr/local/lib/python3.6/dist-packages (from hyperopt>=0.1.1->flair) (0.16.0)\n",
      "Requirement already satisfied: scipy in /usr/local/lib/python3.6/dist-packages (from hyperopt>=0.1.1->flair) (1.3.0)\n",
      "Requirement already satisfied: requests in /usr/local/lib/python3.6/dist-packages (from pytorch-pretrained-bert>=0.6.1->flair) (2.21.0)\n",
      "Requirement already satisfied: boto3 in /usr/local/lib/python3.6/dist-packages (from pytorch-pretrained-bert>=0.6.1->flair) (1.9.167)\n",
      "Collecting sentencepiece (from bpemb>=0.2.9->flair)\n",
      "\u001b[?25l  Downloading https://files.pythonhosted.org/packages/00/95/7f357995d5eb1131aa2092096dca14a6fc1b1d2860bd99c22a612e1d1019/sentencepiece-0.1.82-cp36-cp36m-manylinux1_x86_64.whl (1.0MB)\n",
      "\u001b[K     |████████████████████████████████| 1.0MB 36.6MB/s \n",
      "\u001b[?25hRequirement already satisfied: attrs>=17.4.0 in /usr/local/lib/python3.6/dist-packages (from pytest>=3.6.4->flair) (19.1.0)\n",
      "Requirement already satisfied: setuptools in /usr/local/lib/python3.6/dist-packages (from pytest>=3.6.4->flair) (41.0.1)\n",
      "Requirement already satisfied: atomicwrites>=1.0 in /usr/local/lib/python3.6/dist-packages (from pytest>=3.6.4->flair) (1.3.0)\n",
      "Requirement already satisfied: more-itertools>=4.0.0 in /usr/local/lib/python3.6/dist-packages (from pytest>=3.6.4->flair) (7.0.0)\n",
      "Requirement already satisfied: pluggy<0.8,>=0.5 in /usr/local/lib/python3.6/dist-packages (from pytest>=3.6.4->flair) (0.7.1)\n",
      "Requirement already satisfied: py>=1.5.0 in /usr/local/lib/python3.6/dist-packages (from pytest>=3.6.4->flair) (1.8.0)\n",
      "Requirement already satisfied: smart-open>=1.2.1 in /usr/local/lib/python3.6/dist-packages (from gensim>=3.4.0->flair) (1.8.4)\n",
      "Requirement already satisfied: python-dateutil>=2.1 in /usr/local/lib/python3.6/dist-packages (from matplotlib>=2.2.3->flair) (2.5.3)\n",
      "Requirement already satisfied: kiwisolver>=1.0.1 in /usr/local/lib/python3.6/dist-packages (from matplotlib>=2.2.3->flair) (1.1.0)\n",
      "Requirement already satisfied: cycler>=0.10 in /usr/local/lib/python3.6/dist-packages (from matplotlib>=2.2.3->flair) (0.10.0)\n",
      "Requirement already satisfied: pyparsing!=2.0.4,!=2.1.2,!=2.1.6,>=2.0.1 in /usr/local/lib/python3.6/dist-packages (from matplotlib>=2.2.3->flair) (2.4.0)\n",
      "Requirement already satisfied: joblib>=0.11 in /usr/local/lib/python3.6/dist-packages (from scikit-learn->sklearn->flair) (0.13.2)\n",
      "Requirement already satisfied: decorator>=4.3.0 in /usr/local/lib/python3.6/dist-packages (from networkx->hyperopt>=0.1.1->flair) (4.4.0)\n",
      "Requirement already satisfied: idna<2.9,>=2.5 in /usr/local/lib/python3.6/dist-packages (from requests->pytorch-pretrained-bert>=0.6.1->flair) (2.8)\n",
      "Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.6/dist-packages (from requests->pytorch-pretrained-bert>=0.6.1->flair) (2019.3.9)\n",
      "Requirement already satisfied: chardet<3.1.0,>=3.0.2 in /usr/local/lib/python3.6/dist-packages (from requests->pytorch-pretrained-bert>=0.6.1->flair) (3.0.4)\n",
      "Requirement already satisfied: s3transfer<0.3.0,>=0.2.0 in /usr/local/lib/python3.6/dist-packages (from boto3->pytorch-pretrained-bert>=0.6.1->flair) (0.2.1)\n",
      "Requirement already satisfied: jmespath<1.0.0,>=0.7.1 in /usr/local/lib/python3.6/dist-packages (from boto3->pytorch-pretrained-bert>=0.6.1->flair) (0.9.4)\n",
      "Requirement already satisfied: botocore<1.13.0,>=1.12.167 in /usr/local/lib/python3.6/dist-packages (from boto3->pytorch-pretrained-bert>=0.6.1->flair) (1.12.167)\n",
      "Requirement already satisfied: boto>=2.32 in /usr/local/lib/python3.6/dist-packages (from smart-open>=1.2.1->gensim>=3.4.0->flair) (2.49.0)\n",
      "Requirement already satisfied: docutils>=0.10 in /usr/local/lib/python3.6/dist-packages (from botocore<1.13.0,>=1.12.167->boto3->pytorch-pretrained-bert>=0.6.1->flair) (0.14)\n",
      "Building wheels for collected packages: segtok, mpld3, regex, sqlitedict\n",
      "  Building wheel for segtok (setup.py) ... \u001b[?25l\u001b[?25hdone\n",
      "  Stored in directory: /root/.cache/pip/wheels/15/ee/a8/6112173f1386d33eebedb3f73429cfa41a4c3084556bcee254\n",
      "  Building wheel for mpld3 (setup.py) ... \u001b[?25l\u001b[?25hdone\n",
      "  Stored in directory: /root/.cache/pip/wheels/c0/47/fb/8a64f89aecfe0059830479308ad42d62e898a3e3cefdf6ba28\n",
      "  Building wheel for regex (setup.py) ... \u001b[?25l\u001b[?25hdone\n",
      "  Stored in directory: /root/.cache/pip/wheels/35/e4/80/abf3b33ba89cf65cd262af8a22a5a999cc28fbfabea6b38473\n",
      "  Building wheel for sqlitedict (setup.py) ... \u001b[?25l\u001b[?25hdone\n",
      "  Stored in directory: /root/.cache/pip/wheels/bd/57/d3/907c3ee02d35e66f674ad0106e61f06eeeb98f6ee66a6cc3fe\n",
      "Successfully built segtok mpld3 regex sqlitedict\n",
      "Installing collected packages: regex, segtok, deprecated, mpld3, pytorch-pretrained-bert, sentencepiece, bpemb, sqlitedict, flair\n",
      "Successfully installed bpemb-0.3.0 deprecated-1.2.5 flair-0.4.2 mpld3-0.3 pytorch-pretrained-bert-0.6.2 regex-2019.6.8 segtok-1.5.7 sentencepiece-0.1.82 sqlitedict-1.6.0\n"
     ]
    }
   ],
   "source": [
    "! pip install flair"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 240
    },
    "colab_type": "code",
    "id": "uLgaBlIllg0Y",
    "outputId": "bf8b31f7-5332-4fa0-8928-8fb050a3a6fa"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-06-18 08:18:12,360 Reading data from /content/gdrive/My Drive/SAKI/Exercise_2\n",
      "2019-06-18 08:18:12,362 Train: /content/gdrive/My Drive/SAKI/Exercise_2/train_res_bilou.txt\n",
      "2019-06-18 08:18:12,367 Dev: None\n",
      "2019-06-18 08:18:12,371 Test: /content/gdrive/My Drive/SAKI/Exercise_2/test_res_bilou.txt\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/usr/local/lib/python3.6/dist-packages/ipykernel_launcher.py:20: DeprecationWarning: Call to deprecated function (or staticmethod) load_column_corpus. (Use 'flair.datasets' instead.) -- Deprecated since version 0.4.1.\n",
      "/usr/local/lib/python3.6/dist-packages/flair/data_fetcher.py:312: DeprecationWarning: Call to deprecated function (or staticmethod) read_column_data. (Use 'flair.datasets' instead.) -- Deprecated since version 0.4.1.\n",
      "  train_file, column_format\n",
      "/usr/local/lib/python3.6/dist-packages/flair/data_fetcher.py:318: DeprecationWarning: Call to deprecated function (or staticmethod) read_column_data. (Use 'flair.datasets' instead.) -- Deprecated since version 0.4.1.\n",
      "  test_file, column_format\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[b'<unk>', b'O', b'I-Degree', b'B-Companies_worked_at', b'I-Companies_worked_at', b'B-Degree', b'B-Designation', b'I-Designation', b'<START>', b'<STOP>']\n",
      "Corpus: 31088 train + 3454 dev + 9661 test sentences\n"
     ]
    }
   ],
   "source": [
    "from flair.data import Corpus\n",
    "from flair.data_fetcher import NLPTaskDataFetcher, NLPTask\n",
    "from typing import List\n",
    "\n",
    "\n",
    "# columns of \"gold standard\" ner annotations and text\n",
    "columns = {1:\"ner\",3:\"text\"}\n",
    "\n",
    "# folder where training and test data are\n",
    "data_folder = '/content/gdrive/My Drive/SAKI/Exercise_2'\n",
    "\n",
    "# tag we want to predict\n",
    "tag_type = 'ner'\n",
    "\n",
    "downsample = 1.0 # 1.0 is full data\n",
    "\n",
    "corpus: Corpus = NLPTaskDataFetcher.load_column_corpus(data_folder, columns,\n",
    "                                                              train_file='train_res_bilou.txt',\n",
    "                                                              test_file='test_res_bilou.txt',\n",
    "                                                              dev_file=None).downsample(downsample)                                                  \n",
    "\n",
    "# Make the tag dictionary from the corpus\n",
    "tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)\n",
    "print(tag_dictionary.idx2item)\n",
    "print(corpus)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 370
    },
    "colab_type": "code",
    "id": "LjhlAggj_AES",
    "outputId": "85c2b2a5-cfa3-4e7d-db09-140884113a5a"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-06-18 08:18:23,224 https://s3.eu-central-1.amazonaws.com/alan-nlp/resources/embeddings/glove.gensim.vectors.npy not found in cache, downloading to /tmp/tmpow0nfo5b\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "100%|██████████| 160000128/160000128 [00:07<00:00, 21384086.59B/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-06-18 08:18:31,217 copying /tmp/tmpow0nfo5b to cache at /root/.flair/embeddings/glove.gensim.vectors.npy\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-06-18 08:18:31,475 removing temp file /tmp/tmpow0nfo5b\n",
      "2019-06-18 08:18:31,964 https://s3.eu-central-1.amazonaws.com/alan-nlp/resources/embeddings/glove.gensim not found in cache, downloading to /tmp/tmpvcozhu3n\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "100%|██████████| 21494764/21494764 [00:01<00:00, 12301314.96B/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-06-18 08:18:34,180 copying /tmp/tmpvcozhu3n to cache at /root/.flair/embeddings/glove.gensim\n",
      "2019-06-18 08:18:34,213 removing temp file /tmp/tmpvcozhu3n\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\n",
      "/usr/local/lib/python3.6/dist-packages/smart_open/smart_open_lib.py:398: UserWarning: This function is deprecated, use smart_open.open instead. See the migration notes for details: https://github.com/RaRe-Technologies/smart_open/blob/master/README.rst#migrating-to-the-new-open-function\n",
      "  'See the migration notes for details: %s' % _MIGRATION_NOTES_URL\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-06-18 08:18:36,582 https://s3.eu-central-1.amazonaws.com/alan-nlp/resources/embeddings-v0.4.1/big-news-forward--h2048-l1-d0.05-lr30-0.25-20/news-forward-0.4.1.pt not found in cache, downloading to /tmp/tmphvazziqz\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "100%|██████████| 73034624/73034624 [00:03<00:00, 18988410.72B/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-06-18 08:18:40,904 copying /tmp/tmphvazziqz to cache at /root/.flair/embeddings/news-forward-0.4.1.pt\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-06-18 08:18:41,007 removing temp file /tmp/tmphvazziqz\n",
      "2019-06-18 08:18:48,522 https://s3.eu-central-1.amazonaws.com/alan-nlp/resources/embeddings-v0.4.1/big-news-backward--h2048-l1-d0.05-lr30-0.25-20/news-backward-0.4.1.pt not found in cache, downloading to /tmp/tmpyj_39wlz\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "100%|██████████| 73034575/73034575 [00:03<00:00, 18569269.08B/s]"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-06-18 08:18:52,979 copying /tmp/tmpyj_39wlz to cache at /root/.flair/embeddings/news-backward-0.4.1.pt\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-06-18 08:18:53,100 removing temp file /tmp/tmpyj_39wlz\n"
     ]
    }
   ],
   "source": [
    "# Initialize embeddings\n",
    "from flair.embeddings import TokenEmbeddings, WordEmbeddings, StackedEmbeddings, FlairEmbeddings\n",
    "\n",
    "embedding_types: List[TokenEmbeddings] = [\n",
    "    WordEmbeddings('glove'),\n",
    "    FlairEmbeddings('news-forward'),\n",
    "    FlairEmbeddings('news-backward'),\n",
    "]\n",
    "\n",
    "embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)\n",
    "\n",
    "# Initialize sequence tagger\n",
    "from flair.models import SequenceTagger\n",
    "\n",
    "tagger: SequenceTagger = SequenceTagger(hidden_size=256,\n",
    "                                        embeddings=embeddings,\n",
    "                                        tag_dictionary=tag_dictionary,\n",
    "                                        tag_type=tag_type,\n",
    "                                        use_crf=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 0,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 1514
    },
    "colab_type": "code",
    "id": "_V8jDGKt_Cnv",
    "outputId": "b93e6e0f-d476-49c1-e19f-6558ed47637b"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-06-18 09:53:05,276 ----------------------------------------------------------------------------------------------------\n",
      "2019-06-18 09:53:05,278 Evaluation method: MICRO_F1_SCORE\n",
      "2019-06-18 09:53:05,688 ----------------------------------------------------------------------------------------------------\n",
      "2019-06-18 09:53:06,873 epoch 1 - iter 0/972 - loss 2.85868120\n",
      "2019-06-18 09:53:57,488 epoch 1 - iter 97/972 - loss 1.02157452\n",
      "2019-06-18 09:54:48,248 epoch 1 - iter 194/972 - loss 0.84594419\n",
      "2019-06-18 09:55:40,431 epoch 1 - iter 291/972 - loss 0.76138058\n",
      "2019-06-18 09:56:30,088 epoch 1 - iter 388/972 - loss 0.71832167\n",
      "2019-06-18 09:57:19,477 epoch 1 - iter 485/972 - loss 0.66389715\n",
      "2019-06-18 09:58:09,303 epoch 1 - iter 582/972 - loss 0.64193055\n",
      "2019-06-18 09:59:00,531 epoch 1 - iter 679/972 - loss 0.62498410\n",
      "2019-06-18 09:59:49,662 epoch 1 - iter 776/972 - loss 0.59946235\n",
      "2019-06-18 10:00:38,680 epoch 1 - iter 873/972 - loss 0.57920926\n",
      "2019-06-18 10:01:29,973 epoch 1 - iter 970/972 - loss 0.55927929\n",
      "2019-06-18 10:01:31,457 ----------------------------------------------------------------------------------------------------\n",
      "2019-06-18 10:01:31,460 EPOCH 1 done: loss 0.5592 - lr 0.1000 - bad epochs 0\n",
      "2019-06-18 10:02:27,640 DEV : loss 0.32154831290245056 - score 0.6475\n",
      "2019-06-18 10:05:05,327 TEST : loss 0.3464663326740265 - score 0.648\n",
      "2019-06-18 10:05:11,077 ----------------------------------------------------------------------------------------------------\n",
      "2019-06-18 10:05:12,357 epoch 2 - iter 0/972 - loss 0.22700195\n",
      "2019-06-18 10:06:03,237 epoch 2 - iter 97/972 - loss 0.39378657\n",
      "2019-06-18 10:06:56,126 epoch 2 - iter 194/972 - loss 0.39463417\n",
      "2019-06-18 10:07:46,443 epoch 2 - iter 291/972 - loss 0.39169975\n",
      "2019-06-18 10:08:36,005 epoch 2 - iter 388/972 - loss 0.39069823\n",
      "2019-06-18 10:09:27,022 epoch 2 - iter 485/972 - loss 0.38070822\n",
      "2019-06-18 10:10:17,106 epoch 2 - iter 582/972 - loss 0.38047858\n",
      "2019-06-18 10:11:05,852 epoch 2 - iter 679/972 - loss 0.37361238\n",
      "2019-06-18 10:11:54,659 epoch 2 - iter 776/972 - loss 0.37407620\n",
      "2019-06-18 10:12:45,769 epoch 2 - iter 873/972 - loss 0.36605191\n",
      "2019-06-18 10:13:35,276 epoch 2 - iter 970/972 - loss 0.36327417\n",
      "2019-06-18 10:13:36,838 ----------------------------------------------------------------------------------------------------\n",
      "2019-06-18 10:13:36,842 EPOCH 2 done: loss 0.3629 - lr 0.1000 - bad epochs 0\n",
      "2019-06-18 10:14:32,644 DEV : loss 0.2593117356300354 - score 0.6866\n",
      "2019-06-18 10:17:09,680 TEST : loss 0.2895258069038391 - score 0.6846\n",
      "2019-06-18 10:17:15,414 ----------------------------------------------------------------------------------------------------\n",
      "2019-06-18 10:17:16,709 epoch 3 - iter 0/972 - loss 0.56038886\n",
      "2019-06-18 10:18:09,587 epoch 3 - iter 97/972 - loss 0.28983450\n",
      "2019-06-18 10:18:58,910 epoch 3 - iter 194/972 - loss 0.28585175\n",
      "2019-06-18 10:19:48,449 epoch 3 - iter 291/972 - loss 0.29980443\n",
      "2019-06-18 10:20:40,372 epoch 3 - iter 388/972 - loss 0.31299472\n",
      "2019-06-18 10:21:29,267 epoch 3 - iter 485/972 - loss 0.30872447\n",
      "2019-06-18 10:22:18,330 epoch 3 - iter 582/972 - loss 0.31057056\n",
      "2019-06-18 10:23:08,251 epoch 3 - iter 679/972 - loss 0.31090769\n",
      "2019-06-18 10:23:59,849 epoch 3 - iter 776/972 - loss 0.31294846\n",
      "2019-06-18 10:24:49,170 epoch 3 - iter 873/972 - loss 0.31419553\n",
      "2019-06-18 10:25:38,655 epoch 3 - iter 970/972 - loss 0.31390553\n",
      "2019-06-18 10:25:40,266 ----------------------------------------------------------------------------------------------------\n",
      "2019-06-18 10:25:40,268 EPOCH 3 done: loss 0.3139 - lr 0.1000 - bad epochs 0\n",
      "2019-06-18 10:26:39,258 DEV : loss 0.24319912493228912 - score 0.7057\n",
      "2019-06-18 10:29:16,728 TEST : loss 0.26508328318595886 - score 0.6975\n",
      "2019-06-18 10:29:23,548 ----------------------------------------------------------------------------------------------------\n",
      "2019-06-18 10:29:24,872 epoch 4 - iter 0/972 - loss 0.24768075\n",
      "2019-06-18 10:30:16,506 epoch 4 - iter 97/972 - loss 0.27026448\n",
      "2019-06-18 10:31:06,870 epoch 4 - iter 194/972 - loss 0.26505173\n",
      "2019-06-18 10:31:59,362 epoch 4 - iter 291/972 - loss 0.26808722\n",
      "2019-06-18 10:32:48,496 epoch 4 - iter 388/972 - loss 0.27401957\n",
      "2019-06-18 10:33:37,961 epoch 4 - iter 485/972 - loss 0.27266311\n",
      "2019-06-18 10:34:29,133 epoch 4 - iter 582/972 - loss 0.28116056\n",
      "2019-06-18 10:35:18,045 epoch 4 - iter 679/972 - loss 0.28862500\n",
      "2019-06-18 10:36:07,304 epoch 4 - iter 776/972 - loss 0.28214874\n",
      "2019-06-18 10:36:56,259 epoch 4 - iter 873/972 - loss 0.28201593\n",
      "2019-06-18 10:37:47,265 epoch 4 - iter 970/972 - loss 0.27623696\n",
      "2019-06-18 10:37:48,859 ----------------------------------------------------------------------------------------------------\n",
      "2019-06-18 10:37:48,865 EPOCH 4 done: loss 0.2762 - lr 0.1000 - bad epochs 0\n",
      "2019-06-18 10:38:44,895 DEV : loss 0.2826918661594391 - score 0.6788\n",
      "2019-06-18 10:41:22,568 TEST : loss 0.2800303101539612 - score 0.6759\n",
      "2019-06-18 10:41:22,577 ----------------------------------------------------------------------------------------------------\n",
      "2019-06-18 10:41:23,823 epoch 5 - iter 0/972 - loss 0.62402219\n",
      "2019-06-18 10:42:14,282 epoch 5 - iter 97/972 - loss 0.26564033\n",
      "2019-06-18 10:43:07,206 epoch 5 - iter 194/972 - loss 0.27440776\n",
      "2019-06-18 10:43:57,231 epoch 5 - iter 291/972 - loss 0.27534465\n",
      "2019-06-18 10:44:46,837 epoch 5 - iter 388/972 - loss 0.26528440\n",
      "2019-06-18 10:45:38,020 epoch 5 - iter 485/972 - loss 0.26049523\n",
      "2019-06-18 10:46:27,394 epoch 5 - iter 582/972 - loss 0.26138902\n",
      "2019-06-18 10:47:16,697 epoch 5 - iter 679/972 - loss 0.26539495\n",
      "2019-06-18 10:48:06,101 epoch 5 - iter 776/972 - loss 0.26267800\n",
      "2019-06-18 10:48:58,088 epoch 5 - iter 873/972 - loss 0.25976784\n",
      "2019-06-18 10:49:46,956 epoch 5 - iter 970/972 - loss 0.26157928\n",
      "2019-06-18 10:49:48,520 ----------------------------------------------------------------------------------------------------\n",
      "2019-06-18 10:49:48,523 EPOCH 5 done: loss 0.2616 - lr 0.1000 - bad epochs 1\n",
      "2019-06-18 10:50:44,463 DEV : loss 0.23190419375896454 - score 0.7021\n"
     ]
    }
   ],
   "source": [
    "# 6. initialize trainer\n",
    "from flair.trainers import ModelTrainer\n",
    "\n",
    "trainer: ModelTrainer = ModelTrainer(tagger, corpus)\n",
    "\n",
    "# 7. start training\n",
    "trainer.train('resources/taggers/resume-ner',\n",
    "              learning_rate=0.1,\n",
    "              mini_batch_size=32,\n",
    "              max_epochs=150)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 239
    },
    "colab_type": "code",
    "id": "BaPdGvE1qEPO",
    "outputId": "c447c126-ffde-4592-d000-4a0e187e19a8"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "2019-06-18 08:30:39,512 ----------------------------------------------------------------------------------------------------\n",
      "2019-06-18 08:30:39,516 Testing using best model ...\n",
      "2019-06-18 08:30:39,520 loading file resources/taggers/resume-ner/best-model.pt\n",
      "2019-06-18 08:33:18,502 0.7876\t0.7254\t0.7552\n",
      "2019-06-18 08:33:18,507 \n",
      "MICRO_AVG: acc 0.6067 - f1-score 0.7552\n",
      "MACRO_AVG: acc 0.6199 - f1-score 0.7648666666666667\n",
      "Companies_worked_at tp: 358 - fp: 98 - fn: 158 - tn: 358 - precision: 0.7851 - recall: 0.6938 - accuracy: 0.5831 - f1-score: 0.7366\n",
      "Degree     tp: 115 - fp: 31 - fn: 28 - tn: 115 - precision: 0.7877 - recall: 0.8042 - accuracy: 0.6609 - f1-score: 0.7959\n",
      "Designation tp: 354 - fp: 94 - fn: 127 - tn: 354 - precision: 0.7902 - recall: 0.7360 - accuracy: 0.6157 - f1-score: 0.7621\n",
      "2019-06-18 08:33:18,508 ----------------------------------------------------------------------------------------------------\n",
      "0.7552\n"
     ]
    }
   ],
   "source": [
    "from flair.training_utils import EvaluationMetric\n",
    "from typing import List, Union\n",
    "from pathlib import Path\n",
    "from flair.trainers import ModelTrainer\n",
    "\n",
    "trainer: ModelTrainer = ModelTrainer(tagger, corpus)\n",
    "model = trainer.final_test(Path(\"resources/taggers/resume-ner/\"), True, EvaluationMetric.MICRO_F1_SCORE,32)\n",
    "print(model)"
   ]
  }
 ],
 "metadata": {
  "accelerator": "GPU",
  "colab": {
   "collapsed_sections": [],
   "name": "3. Screenshot",
   "provenance": [],
   "version": "0.3.2"
  },
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 1
}

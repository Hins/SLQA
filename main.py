# coding=UTF-8

from allennlp import commands

import sys
import json

if len(sys.argv) < 1:
    sys.exit()

with open(sys.argv[1], encoding='utf-8') as f:
    json_obj = json.load(f)
    if json_obj.get("version") is None:
        json_obj["version"] = "1"
    if json_obj.get("data") is None or not hasattr(json_obj.get("data"), '__iter__'):
        sys.exit() 
    new_obj = []
    for element in json_obj.get("data"):
        name = ""
        if element.get("title") is None:
            name = "default"
        else:
            name = element.get("title")
        ident = "1"
        if element.get("id") is None:
            ident= "1"
        else:
            ident = element.get("id")
        source = "dataTang"
        filename = "dataTang"
        if element.get("paragraphs") is None or not hasattr(element.get("paragraphs"), '__iter__'):
            continue
        sub_obj = {}
        for para in element.get("paragraphs"):
            if para.get("context") is None:
                continue
            if para.get("qas") is None or not hasattr(para.get("qas"), '__iter__'):
                continue
            sub_obj["story"] = para.get("context")
            questions_arr = []
            answers_arr = []
            counter = 1
            for qas in para.get("qas"):
                if qas.get("question") is None:
                    continue
                if qas.get("answers") is None or not hasattr(qas.get("answers"), '__iter__'):
                    continue
                question_obj = {}
                question_obj["input_text"] = qas.get("question")
                question_obj["turn_id"] = counter
                questions_arr.append(question_obj)
                answer_obj = {}
                for ans in qas.get("answers"):
                    answer_obj["span_text"] = ans["text"]
                    answer_obj["span_start"] = ans["answer_start"]
                    answer_obj["span_end"] = ans["answer_start"] + len(ans["text"])
                    answer_obj["input_text"] = ans["text"]
                    answer_obj["turn_id"] = counter
                answers_arr.append(answer_obj)
                counter += 1
            sub_obj["questions"] = questions_arr
            sub_obj["answers"] = answers_arr
            sub_obj["source"] = source
            sub_obj["id"] = ident
            sub_obj["filename"] = filename
            sub_obj["name"] = name
            new_obj.append(sub_obj)
    json_obj["data"] = new_obj
    if json_obj.get("source") is None:
        json_obj["source"] = "dataTang"

with open("./test.json", 'w') as write_f:
    json.dump(json_obj, write_f, indent=4, ensure_ascii=False)

commands.main()


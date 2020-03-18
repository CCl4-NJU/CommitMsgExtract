from scrapy.cmdline import execute
execute(["scrapy","crawl","login","-o","msg.json"])

# f = open("G:\\scpy\\login\\login\\json.txt")
# wf = open("result.txt","w")
# for line in f:
#     path = line.split("\"")[-2]
#     wf.writelines(path+"\n")
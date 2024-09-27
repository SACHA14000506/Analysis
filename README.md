python3 fetch.py --issue-code JENKINS --jira-project issues.jenkins-ci.org
将Jenkins这个项目的一些issues数据下载到本地
git clone https://github.com/jenkinsci/jenkins.git
clone到本地Jenkins这个项目的本地Repo
python3 git_log_to_array.py --from-commit <SHA-1_of_initial_commit> --repo-path ./~/jenkins
<SHA-1_of_initial_commit>  =  git rev-parse HEAD
将Git log转成后续环节可以处理的格式,生成gitlog.json文件
python3 find_bug_fixes.py --gitlog gitlog.json --issue-list issues --gitlog-pattern "JENKINS-{nbr}\D|#{nbr}\D|HUDSON-{nbr}\D"
生成issue_list.json文件，里面记录了所有和修复issue相关的commit，把所有修复issue的commit找到
gradle build && gradle fatJar编译
jcenter，compile过期，需修改
java -jar szz_find_bug_introducers-0.1.jar -i issue_list.json -r ./~/jenkins
得到fix_and_introducers_pairs.json给出了修复和引入Bug的commit对，commits.json文件包含所有被指责为引入错误但还未经任何分析的提交。
训练分类器进行即时错误预测
python3 assemble_code_churns.py --repository /home/cass/Webstorm_project/SZZUnleashed/jenkins
提取的特征：Total lines of code—所有更改的文件总共有多少行代码；Churned lines of code- 已插入的代码行数；Deleted lines of code已删除的代码行数；Number of Files— 已更改的文件总数。
python3 assemble_diffusion_features.py --repository /home/cass/Webstorm_project/SZZUnleashed/jenkins
修改的子系统的数量；已修改的子目录的数量；变化的熵
python3 assemble_experience_features.py --repository /home/cass/Webstorm_project/SZZUnleashed/jenkins --save-graph
总体体验；最近的经历。
python3 assemble_history_features.py --repository /home/cass/Webstorm_project/SZZUnleashed/jenkins  --save-graph
文件中的作者数量。作者做出贡献之间的时间间隔。上次提交之间的唯一更改的数量。

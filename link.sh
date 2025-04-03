export HF_HOME=/mnt/petrelfs/jiangbowen/algTool/huggingface # change to YOURS

cd $HF_HOME/hub

for dn in /mnt/hwfile/opencompass/checkpoints/llm/hf_hub/models--*;
do
  echo $dn     
  ln -snf $dn
done
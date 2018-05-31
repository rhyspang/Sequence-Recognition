old_dir=`pwd`
cd `dirname $0`
echo "Add PYTHONPATH: `pwd`"
export PYTHONPATH=$PYTHONPATH:`pwd`
cd $old_dir
unset old_dir

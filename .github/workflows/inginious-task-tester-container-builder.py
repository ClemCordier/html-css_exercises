#! /bin/env python3

import subprocess
import os

containers = os.environ.get('REQUIRED', 'base').split(' ')
container_names = []
for container in containers:
    container_name = 'ingi/inginious-c-%s:latest' % container
    container_names.append(container_name)
    subprocess.run('docker build -t {container_name} {base_dir}/{sub_dir}/{container}'.format(
        container_name=container_name,
        container=container,
        base_dir='${INGINIOUS}' if container == 'base' else '${CONTAINERS}',
        sub_dir='base-containers' if container == 'base' else 'grading'),
    shell=True)
subprocess.run('docker save %s -o ${INGINIOUS_IMAGES}' % ' '.join(container_names), shell=True)

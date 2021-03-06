#!/usr/bin/env bash

cat <<EOF > /etc/init.d/disable-thp
#!/bin/bash

    ### BEGIN INIT INFO
    # Provides:          disable-thp
    # Required-Start:    \$local_fs
    # Required-Stop:
    # X-Start-Before:
    # Default-Start:     2 3 4 5
    # Default-Stop:      0 1 6
    # Short-Description: Disable THP
    # Description:       disables Transparent Huge Pages (THP) on boot
    ### END INIT INFO

    case \$1 in
    start)
    if [ -d /sys/kernel/mm/transparent_hugepage ]; then
    echo 'never' > /sys/kernel/mm/transparent_hugepage/enabled
    echo 'never' > /sys/kernel/mm/transparent_hugepage/defrag
    elif [ -d /sys/kernel/mm/redhat_transparent_hugepage ]; then
    echo 'never' > /sys/kernel/mm/redhat_transparent_hugepage/enabled
    echo 'never' > /sys/kernel/mm/redhat_transparent_hugepage/defrag
    else
    return 0
    fi
    ;;
    esac
EOF

sudo chmod 755 /etc/init.d/disable-thp
sudo service disable-thp start
sudo update-rc.d disable-thp defaults
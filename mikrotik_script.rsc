# تحديد المتغيرات
:local apiUrl "https://your-flask-api.onrender.com/vlan_data"
:local routerId [/system identity get name]

# جمع بيانات الاستهلاك لكل VLAN
:local vlanData ""
/interface vlan print without-paging do={
    :local vlanName $name
    :local vlanId $vlan-id
    :local vlanInterface $interface

    /interface monitor-traffic interface=$vlanName once do={
        :local rxBytes $"rx-byte"
        :local txBytes $"tx-byte"
        :set vlanData ($vlanData . "{\"name\":\"$vlanName\",\"id\":$vlanId,\"interface\":\"$vlanInterface\",\"rxBytes\":$rxBytes,\"txBytes\":$txBytes},")
    }
}

# إزالة الفاصلة الأخيرة
:set vlanData [:pick $vlanData 0 ([:len $vlanData] - 1)]
:set vlanData ("{\"router_id\":\"$routerId\",\"vlans\":[" . $vlanData . "]}")

# إرسال البيانات إلى API
/tool fetch url="$apiUrl" http-method=post http-header-field="Content-Type: application/json" http-data=$vlanData

# سجل الأحداث
:log info "VLAN data sent to API: $apiUrl"

from flask_login import login_required, login_user, logout_user
from flask import Blueprint, render_template, request, jsonify, url_for, redirect
import os
from sqlalchemy import and_, func, or_
from .models import Location, User, db, Equipment, Department


admin = Blueprint('admin', __name__)


@admin.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "GET":
        return render_template("admin/upload.html")
    else:
        my_file = request.files.get("my_file")
        new_file = os.path.join("files", my_file.filename)
        my_file.save(new_file)
        RET = {
            "code": 0,
            "filename": my_file.filename,
            "msg": "上传成功"
        }
        return jsonify(RET)


@admin.route("/office", methods=["GET", "POST"])
def office():
    if request.method == "GET":

        return render_template("admin/office.html")
    else:
        computer_count = db.session.query(func.count(Equipment.id)).filter(
            Equipment.category_id==8).scalar()

        computer = Equipment.query.filter(
            Equipment.category_id==8).limit(5).all()
        computer_list = []
        for c in computer:
            obj = {"name": c.name, "model": c.model, 
                   "asset_number": c.asset_number, "asset_status": c.asset_status}
            computer_list.append(obj)
        printer_list = []
        printer_count = db.session.query(func.count(Equipment.id)).filter(
            Equipment.category_id==9).scalar()
        printer = Equipment.query.filter(
            Equipment.category_id==9).limit(5).all()
        for p in printer:
            obj = {"name": p.name, "model": p.model, 
                   "asset_number": p.asset_number, "asset_status": p.asset_status}
            printer_list.append(obj)
        camera_list = []
        camera_count = db.session.query(func.count(Equipment.id)).filter(
            Equipment.category_id==5).scalar()
        camera = Equipment.query.filter(
            Equipment.category_id==5).limit(5).all()
        for c in camera:
            obj = {"name": c.name, "model": c.model,
                   "asset_number": c.asset_number, "asset_status": c.asset_status}
            camera_list.append(obj)
        # 录像机
        video_recorder_count = db.session.query(func.count(Equipment.id)).filter(
            Equipment.category_id==4).scalar()
        video_recorder = Equipment.query.filter(
            Equipment.category_id==4).limit(5).all()
        video_recorder_list = []
        for c in video_recorder:
            obj = {"name": c.name, "model": c.model,
                   "asset_number": c.asset_number, "asset_status": c.asset_status}
            video_recorder_list.append(obj)
        # 集团派驻
        stationing_count = db.session.query(func.count(Equipment.id)).filter(
            Equipment.department_id==1).scalar()
        # print(stationing_count)
        stationing = Equipment.query.filter(
            Equipment.department_id==1).limit(5).all()
        stationing_list = []
        for c in stationing:
            obj = {"name": c.name, "model": c.model,
                   "asset_number": c.asset_number, "asset_status": c.asset_status}
            stationing_list.append(obj)
        # 行政部
        integrated_count = db.session.query(func.count(Equipment.id)).filter(
            Equipment.department_id==2).scalar()
        integrated = Equipment.query.filter(
            Equipment.department_id==2).limit(5).all()
        integrated_list = []
        for c in integrated:
            obj = {"name": c.name, "model": c.model,
                   "asset_number": c.asset_number, "asset_status": c.asset_status}
            integrated_list.append(obj)
        # 财务部
        finance_count = db.session.query(func.count(Equipment.id)).filter(
            Equipment.department_id==3).scalar()
        finance = Equipment.query.filter(
            Equipment.department_id==3).limit(5).all()
        finance_list = []
        for c in finance:
            obj = {"name": c.name, "model": c.model,
                   "asset_number": c.asset_number, "asset_status": c.asset_status}
            finance_list.append(obj)
        # 运营部
        operation_count = db.session.query(func.count(Equipment.id)).filter(
            Equipment.department_id==4).scalar()
        operation = Equipment.query.filter(
            Equipment.department_id==4).limit(5).all()
        operation_list = []
        for c in operation:
            obj = {"name": c.name, "model": c.model,
                   "asset_number": c.asset_number, "asset_status": c.asset_status}
            operation_list.append(obj)
        # 按位置
        # 领导办公室
        location_leader_count = db.session.query(func.count(Equipment.id)).filter(
            Equipment.location_id==5).scalar()
        location_leader = Equipment.query.filter(
            Equipment.location_id==5).limit(5).all()
        location_leader_list = []
        for c in location_leader:
            obj = {"name": c.name, "model": c.model,
                   "asset_number": c.asset_number, "asset_status": c.asset_status}
            location_leader_list.append(obj)
        # 运营办公室
        location_operate_count = db.session.query(func.count(Equipment.id)).filter(
            Equipment.location_id==6).scalar()
        location_operate = Equipment.query.filter(
            Equipment.location_id==6).limit(5).all()
        location_operate_list = []
        for c in location_operate:
            obj = {"name": c.name, "model": c.model,
                   "asset_number": c.asset_number, "asset_status": c.asset_status}
            location_operate_list.append(obj)
        # 综合办公室
        location_integrated_count = db.session.query(func.count(Equipment.id)).filter(
            Equipment.location_id==7).scalar()
        location_integrated = Equipment.query.filter(
            Equipment.location_id==7).limit(5).all()
        location_integrated_list = []
        for c in location_integrated:
            obj = {"name": c.name, "model": c.model,
                   "asset_number": c.asset_number, "asset_status": c.asset_status}
            location_integrated_list.append(obj)
        # 财务办公室
        location_finance_count = db.session.query(func.count(Equipment.id)).filter(
            Equipment.location_id==8).scalar()
        location_finance = Equipment.query.filter(
            Equipment.location_id==8).limit(5).all()
        location_finance_list = []
        for c in location_finance:
            obj = {"name": c.name, "model": c.model,
                   "asset_number": c.asset_number, "asset_status": c.asset_status}
            location_finance_list.append(obj)

        RET = {
            "computer_count": computer_count,
            "computer_list": computer_list,
            "printer_count": printer_count,
            "printer_list": printer_list,
            "camera_count": camera_count,
            "camera_list": camera_list,
            "video_recorder_count": video_recorder_count,
            "video_recorder_list": video_recorder_list,
            "stationing_count": stationing_count,
            "stationing_list": stationing_list,
            "integrated_count": integrated_count,
            "integrated_list": integrated_list,
            "finance_count": finance_count,
            "finance_list": finance_list,
            "operation_count": operation_count,
            "operation_list": operation_list,
            "location_leader_count":location_leader_count,
            "location_leader_list":location_leader_list,
            "location_operate_count":location_operate_count,
            "location_operate_list":location_operate_list,
            "location_integrated_count":location_integrated_count,
            "location_integrated_list":location_integrated_list,
            "location_finance_count":location_finance_count,
            "location_finance_list":location_finance_list
        }
        return jsonify(RET)


@admin.route("/second_line", methods=["POST"])
def second_line():
    handheld_count = db.session.query(func.count(Equipment.id)).filter(
        Equipment.category_id==1).scalar()
    handheld = Equipment.query.filter(Equipment.category_id==1).limit(5).all()
    handheld_list = []
    for c in handheld:
        obj = {"name": c.name, "model": c.model,
               "asset_number": c.asset_number, "asset_status": c.asset_status}
        handheld_list.append(obj)

    AP_count = db.session.query(func.count(Equipment.id)).filter(
        Equipment.category_id==7).scalar()
    AP = Equipment.query.filter(Equipment.category_id==7).limit(5).all()
    AP_list = []
    for c in AP:
        obj = {"name": c.name, "model": c.model, 
               "asset_number": c.asset_number, "asset_status": c.asset_status}
        AP_list.append(obj)
    # 投影仪
    projector_count = db.session.query(func.count(Equipment.id)).filter(
        Equipment.category_id==11).scalar()
    projector = Equipment.query.filter(
        Equipment.category_id==11).limit(5).all()
    projector_list = []
    for c in projector:
        obj = {"name": c.name, "model": c.model, 
               "asset_number": c.asset_number, "asset_status": c.asset_status}
        projector_list.append(obj)
    # 机柜
    cabinet_count = db.session.query(func.count(Equipment.id)).filter(
        Equipment.category_id==10).scalar()
    cabinet = Equipment.query.filter(
        Equipment.category_id==10).limit(5).all()
    cabinet_list = []
    for c in cabinet:
        obj = {"name": c.name, "model": c.model, 
               "asset_number": c.asset_number, "asset_status": c.asset_status}
        cabinet_list.append(obj)
    RET = {
        "handheld_count": handheld_count,
        "handheld_list": handheld_list,
        "AP_count": AP_count,
        "AP_list": AP_list,
        "projector_count": projector_count,
        "projector_list": projector_list,
        "cabinet_count": cabinet_count,
        "cabinet_list": cabinet_list
    }
    return jsonify(RET)

@admin.route("/third_line", methods=["POST"])
def third_line():
    # 不间断电源
    UPS_count = db.session.query(func.count(Equipment.id)).filter(
        Equipment.category_id==3).scalar()
    UPS = Equipment.query.filter(Equipment.category_id==3).limit(5).all()
    UPS_list = []
    for c in UPS:
        obj = {"name": c.name, "model": c.model, 
               "asset_number": c.asset_number, "asset_status": c.asset_status}
        UPS_list.append(obj)

    switch_list = []
    switch_count = db.session.query(func.count(Equipment.id)).filter(
        Equipment.category_id==2).scalar()
    switch = Equipment.query.filter(
        Equipment.category_id==2).limit(5).all()
    for s in switch:
        obj = {"name": s.name, "model": s.model, 
               "asset_number": s.asset_number, "asset_status": s.asset_status}
        switch_list.append(obj)

    # 路由器
    router_count = db.session.query(func.count(Equipment.id)).filter(
        Equipment.category_id==6).scalar()
    router = Equipment.query.filter(Equipment.category_id==6).limit(5).all()
    router_list = []
    for c in router:
        obj = {"name": c.name, "model": c.model,
               "asset_number": c.asset_number, "asset_status": c.asset_status}
        router_list.append(obj)
    # 其它
    other_count = db.session.query(func.count(Equipment.id)).filter(Equipment.category_id==12).scalar()
    other = Equipment.query.filter(Equipment.category_id==12).limit(5).all()
    other_list = []
    for c in other:
        obj = {"name": c.name, "model": c.model, 
               "asset_number": c.asset_number, "asset_status": c.asset_status}
        other_list.append(obj)
    RET = {
        "UPS_count": UPS_count,
        "UPS_list": UPS_list,
        "switch_count": switch_count,
        "switch_list": switch_list,
        "router_count": router_count,
        "router_list": router_list,
        "other_count": other_count,
        "other_list": other_list
    }
    return jsonify(RET)

@admin.route("/department_second_line", methods=["POST"])
def department_second_line():
    sorting_count = db.session.query(func.count(Equipment.id)).filter(
            Equipment.department_id==5).scalar()
    sorting = Equipment.query.filter(
        Equipment.department_id==5).limit(5).all()
    sorting_list = []
    for c in sorting:
        obj = {"name": c.name, "model": c.model, 
                "asset_number": c.asset_number, "asset_status": c.asset_status}
        sorting_list.append(obj)
    
    # 计划办公室
    planning_count = db.session.query(func.count(Equipment.id)).filter(
            Equipment.department_id==6).scalar()
    planning = Equipment.query.filter(
        Equipment.department_id==6).limit(5).all()
    planning_list = []
    for c in planning:
        obj = {"name": c.name, "model": c.model, 
                "asset_number": c.asset_number, "asset_status": c.asset_status}
        planning_list.append(obj)

    # 仓储部门
    storage_count = db.session.query(func.count(Equipment.id)).filter(
            Equipment.department_id==7).scalar()
    storage = Equipment.query.filter(
        Equipment.department_id==7).limit(5).all()
    storage_list = []
    for c in storage:
        obj = {"name": c.name, "model": c.model, 
                "asset_number": c.asset_number, "asset_status": c.asset_status}
        storage_list.append(obj)
    # 人事部
    personnel_count = db.session.query(func.count(Equipment.id)).filter(
            Equipment.department_id==8).scalar()
    personnel = Equipment.query.filter(
        Equipment.department_id==8).limit(5).all()
    personnel_list = []
    for c in personnel:
        obj = {"name": c.name, "model": c.model, 
                "asset_number": c.asset_number, "asset_status": c.asset_status}
        personnel_list.append(obj)

    RET = {
        "sorting_count": sorting_count,
        "sorting_list": sorting_list,
        "planning_count": planning_count,
        "planning_list": planning_list,
        "storage_count": storage_count,
        "storage_list": storage_list,
        "personnel_count":personnel_count,
        "personnel_list":personnel_list
    }
    return jsonify(RET)

@admin.route("/location_second_line", methods=["POST"])
def location_second_line():
    location_business_count = db.session.query(func.count(Equipment.id)).filter(
            Equipment.location_id==9).scalar()
    location_business = Equipment.query.filter(
        Equipment.location_id==9).limit(5).all()
    location_business_list = []
    for c in location_business:
        obj = {"name": c.name, "model": c.model, 
                "asset_number": c.asset_number, "asset_status": c.asset_status}
        location_business_list.append(obj)
    
    # 计划办公室
    location_planning_count = db.session.query(func.count(Equipment.id)).filter(
            Equipment.location_id==15).scalar()
    location_planning = Equipment.query.filter(
        Equipment.location_id==15).limit(5).all()
    location_planning_list = []
    for c in location_planning:
        obj = {"name": c.name, "model": c.model, 
                "asset_number": c.asset_number, "asset_status": c.asset_status}
        location_planning_list.append(obj)

    # 仓储部门
    location_storage_count = db.session.query(func.count(Equipment.id)).filter(
            Equipment.location_id==16).scalar()
    location_storage = Equipment.query.filter(
        Equipment.location_id==16).limit(5).all()
    location_storage_list = []
    for c in location_storage:
        obj = {"name": c.name, "model": c.model, 
                "asset_number": c.asset_number, "asset_status": c.asset_status}
        location_storage_list.append(obj)

    location_fis_count = db.session.query(func.count(Equipment.id)).filter(
            Equipment.location_id==13).scalar()
    location_fis = Equipment.query.filter(
        Equipment.location_id==13).limit(5).all()
    location_fis_list = []
    for c in location_fis:
        obj = {"name": c.name, "model": c.model, 
                "asset_number": c.asset_number, "asset_status": c.asset_status}
        location_fis_list.append(obj)

    RET = {
        "location_business_count": location_business_count,
        "location_business_list": location_business_list,
        "location_planning_count": location_planning_count,
        "location_planning_list": location_planning_list,
        "location_storage_count": location_storage_count,
        "location_storage_list": location_storage_list,
        "location_fis_count":location_fis_count,
        "location_fis_list":location_fis_list
    }
    return jsonify(RET)

@admin.route("/location_third_line", methods=["POST"])
def location_third_line():
    location_receive_count = db.session.query(func.count(Equipment.id)).filter(
            Equipment.location_id==14).scalar()
    location_receive = Equipment.query.filter(
        Equipment.location_id==14).limit(5).all()
    location_receive_list = []
    for c in location_receive:
        obj = {"name": c.name, "model": c.model, 
                "asset_number": c.asset_number, "asset_status": c.asset_status}
        location_receive_list.append(obj)
    
    # 
    location_network_count = db.session.query(func.count(Equipment.id)).filter(
            Equipment.location_id==17).scalar()
    location_network = Equipment.query.filter(
        Equipment.location_id==17).limit(5).all()
    location_network_list = []
    for c in location_network:
        obj = {"name": c.name, "model": c.model, 
                "asset_number": c.asset_number, "asset_status": c.asset_status}
        location_network_list.append(obj)

    # 
    location_W_guard_count = db.session.query(func.count(Equipment.id)).filter(
            Equipment.location_id==1).scalar()
    location_W_guard = Equipment.query.filter(
        Equipment.location_id==1).limit(5).all()
    location_W_guard_list = []
    for c in location_W_guard:
        obj = {"name": c.name, "model": c.model, 
                "asset_number": c.asset_number, "asset_status": c.asset_status}
        location_W_guard_list.append(obj)

    location_S_guard_count = db.session.query(func.count(Equipment.id)).filter(
            Equipment.location_id==2).scalar()
    location_S_guard = Equipment.query.filter(
        Equipment.location_id==2).limit(5).all()
    location_S_guard_list = []
    for c in location_S_guard:
        obj = {"name": c.name, "model": c.model, 
                "asset_number": c.asset_number, "asset_status": c.asset_status}
        location_S_guard_list.append(obj)

    RET = {
        "location_receive_count": location_receive_count,
        "location_receive_list": location_receive_list,
        "location_network_count": location_network_count,
        "location_network_list": location_network_list,
        "location_W_guard_count": location_W_guard_count,
        "location_W_guard_list": location_W_guard_list,
        "location_S_guard_count":location_S_guard_count,
        "location_S_guard_list":location_S_guard_list
    }
    return jsonify(RET)

@admin.route("/location_fourth_line", methods=["POST"])
def location_fourth_line():
    location_hall_count = db.session.query(func.count(Equipment.id)).filter(
            Equipment.location_id==3).scalar()
    location_hall = Equipment.query.filter(
        Equipment.location_id==3).limit(5).all()
    location_hall_list = []
    for c in location_hall:
        obj = {"name": c.name, "model": c.model, 
                "asset_number": c.asset_number, "asset_status": c.asset_status}
        location_hall_list.append(obj)
    
    # 
    location_canteen_count = db.session.query(func.count(Equipment.id)).filter(
            Equipment.location_id==4).scalar()
    location_canteen = Equipment.query.filter(
        Equipment.location_id==4).limit(5).all()
    location_canteen_list = []
    for c in location_canteen:
        obj = {"name": c.name, "model": c.model, 
                "asset_number": c.asset_number, "asset_status": c.asset_status}
        location_canteen_list.append(obj)

    # 
    location_small_meeting_count = db.session.query(func.count(Equipment.id)).filter(
            Equipment.location_id==10).scalar()
    location_small_meeting = Equipment.query.filter(
        Equipment.location_id==10).limit(5).all()
    location_small_meeting_list = []
    for c in location_small_meeting:
        obj = {"name": c.name, "model": c.model, 
                "asset_number": c.asset_number, "asset_status": c.asset_status}
        location_small_meeting_list.append(obj)

    location_meeting_count = db.session.query(func.count(Equipment.id)).filter(
            Equipment.location_id==11).scalar()
    location_meeting = Equipment.query.filter(
        Equipment.location_id==11).limit(5).all()
    location_meeting_list = []
    for c in location_meeting:
        obj = {"name": c.name, "model": c.model, 
                "asset_number": c.asset_number, "asset_status": c.asset_status}
        location_meeting_list.append(obj)

    RET = {
        "location_hall_count": location_hall_count,
        "location_hall_list": location_hall_list,
        "location_canteen_count": location_canteen_count,
        "location_canteen_list": location_canteen_list,
        "location_small_meeting_count": location_small_meeting_count,
        "location_small_meeting_list": location_small_meeting_list,
        "location_meeting_count":location_meeting_count,
        "location_meeting_list":location_meeting_list
    }
    return jsonify(RET)

@admin.route("/location_fifth_line", methods=["POST"])
def location_fifth_line():
    location_production_count = db.session.query(func.count(Equipment.id)).filter(
            Equipment.location_id==12).scalar()
    location_production = Equipment.query.filter(
        Equipment.location_id==12).limit(5).all()
    location_production_list = []
    for c in location_production:
        obj = {"name": c.name, "model": c.model, 
                "asset_number": c.asset_number, "asset_status": c.asset_status}
        location_production_list.append(obj)
    
    

    RET = {
        
        "location_production_count":location_production_count,
        "location_production_list":location_production_list
    }
    return jsonify(RET)
@admin.route("/detail/<name>", methods=["GET"])
def detail(name):
    if name=="8":
        res=db.session.query(Equipment.name,Equipment.model,Department.name, Location.name,Equipment.user,Equipment.IPaddress,Equipment.asset_number,Equipment.asset_status,Equipment.category_id).join(Department,Equipment.department_id==Department.id).join(Location,Equipment.location_id==Location.id).filter(
            Equipment.category_id==8).order_by(Department.name,Location.name).all()
        return render_template("admin/detail.html",res=res)
    else:
        resu=db.session.query(Equipment.name,Equipment.model,Department.name, Location.name,Equipment.asset_number,Equipment.asset_status).join(Department,Equipment.department_id==Department.id).join(Location,Equipment.location_id==Location.id).filter(
            Equipment.category_id==int(name)).order_by(Department.name,Location.name).all()

        return render_template("admin/detail.html",resu=resu)

@admin.route("/department/<name>", methods=["GET"])
def department(name):
    
    res=db.session.query(Equipment.name,Equipment.model,Department.name, Location.name,Equipment.asset_number,Equipment.asset_status).join(Location,Equipment.location_id==Location.id).join(Department,Equipment.department_id==Department.id).filter(
            Department.id==name).all()
    
    return render_template("admin/department_detail.html",res=res)

@admin.route("/location/<id>", methods=["GET"])
def location(id):
    
    res=db.session.query(Equipment.name,Equipment.model,Department.name, Location.name,Equipment.asset_number,Equipment.asset_status).join(Location,Equipment.location_id==Location.id).join(Department,Equipment.department_id==Department.id).filter(
            Location.id==id).all()
    
    return render_template("admin/location_detail.html",res=res)
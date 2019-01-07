# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from .models import Person
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


def user(request, pk):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        return insert(request, data)
    elif request.method == 'GET':
        if pk:
            return display(request, pk)
    elif request.method == 'PUT':
        if pk:
            return update(request, pk)
    elif request.method == 'DELETE':
        if pk:
            return delete(request, pk)
    else:
        return other(request)


def insert(request, data):
    if data['f_name'] and data['l_name']:
        obj = Person()
        obj.first_name = data['f_name']
        obj.last_name = data['l_name']
        obj.save()
        return response(type='Insert', status=200, content=dict(""), msg="Success")
    else:
        return response(type='Insert', status=201, content=dict(content="Not a Valid data"), msg="Fields are Not Filed")
    return response(type='Insert', status=201, content=dict(content="Can't Inserted"), msg="Failed")


def display(request, pk):
    try:
        obj = Person.objects.get(id=pk)
        return response(type='Display', status=200, content=dict(F_name=obj.first_name, L_name=obj.last_name, id=obj.id),
                        msg="Success")
    except Exception as e:
        return response(type='Display', status=201, content=dict(content="Id is not there"),
                        msg="Failed")


def update(request, pk):
    data = json.loads(request.body.decode('utf-8'))
    if data['f_name'] and data['l_name']:
        try:
            obj = Person.objects.get(id=pk)
            obj.first_name = data['f_name']
            obj.last_name = data['l_name']
            obj.save()
            print obj.first_name
            return response(type='Update', status=200, content=dict(F_name=obj.first_name, L_name=obj.last_name, id=pk),
                            msg="Success")
        except Exception as e:
            return response(type='Update', status=201, content={"content":"Id was not matched"}, msg="Failed")


def delete(request, pk):
    try:
        obj = Person.objects.get(id=pk).delete()
        return response(type='Delete', code=200, content={"content": "Value Deleted", "id":pk}, msg="Success")
    except Exception as e:
        return response(type='Delete', code=201, content={"content": "Id was not available"}, msg="Failed")


def other(request):
    return response(type="other", status=404, content=dict(content="Not valid method"), msg="Method Error")


def response(type, status, content, msg=None):
    res = {}
    print ("type", type, "msg", msg)
    if type == "Insert":
        if msg == "Success":
            res['content'] = content
            res['response'] = dict(code=status, message="Successfully Created")
        elif msg is "NotFilled":
            res['content'] = content
            res['response'] = dict(code=status, message=msg)
    elif type == "Display":
        if msg == "Success":
            res['content'] = content
            res['response'] = dict(code=200, message=msg)
        elif msg == "Failed":
            res['content'] = content
            res['response'] = dict(code=201, message=msg)
    elif type == "Update":
        if msg == "Success":
            res['content'] = content
            res['response'] = dict(code=200, message=msg)
        elif msg == "Failed":
            res['content'] = content
            res['response'] = dict(code=201, message=msg)
    elif type == "Delete":
        if msg == "Success":
            res['content'] = content
            res['response'] = dict(code=200, message=msg)
        elif msg == "Failed":
            res['content'] = content
            res['response'] = dict(code=201, message=msg)
    elif type == "other":
        res['content'] = content
        res['response'] = dict(code=status, message=msg)
    return JsonResponse(res, safe=False)

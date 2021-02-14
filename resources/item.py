from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    fresh_jwt_required
)
from models.item import ItemModel

import pandas as pd
import json
import xlsxwriter


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id."
    )

    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @fresh_jwt_required
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {'items': items}, 200
        return {
            'items': [item['name'] for item in items],
            'message': 'More data available if you log in.'
        }, 200


class ItemJson(Resource):
    def get(self):
        items = [item.json() for item in ItemModel.find_all()]
        df = pd.DataFrame(items)

        #a_json = json.loads(json_string)
        #df = pd.DataFrame.from_dict(a_json, orient="index")
        
        #dd = pd.read_json(datam,orient='columns')
        
        #result = df.to_json(orient="values")
        #parsed = json.loads(result)
        #dd = json.dumps(parsed, indent=2) 

        #dd = df.to_markdown()                                  #Output markdown with a tabulate option.
        #dd = df.to_csv(index=False)                            #Csv formated data
        
        #*orient = 'records/index/values/table/columns(default)'
        #df.to_json(r'D:\jsonfile.json')                        #Copy to json file
        #df.to_json(r'D:\jsonfile.json', orient='split')        #Copy to json file
        #result = df.to_json(orient="table")
        ##df.to_excel(r'D:\jsonfile.xlsx', engine='xlsxwriter') #Copy to xlsx file
        
        #compression_opts = dict(method='zip', archive_name='out.csv')
        #df.to_csv('out.zip', index=False, compression=compression_opts)

        

        dd = df.describe() ##df.count()
        #dd = df.describe(include=['object'])
        #dd = df.corr()     #Correlation Matrix Of Values
        #dd = df.head(2)
        #dd = df.cov()       #Covariance Matrix Of Values
        #dd = df.mean(axis=0)    #returns the mean of every single column
        #results = dd.to_csv(index='true')
        
        results = dd.to_json()
        #results = dd.to_json(index=False)

        return {'items':results}, 200
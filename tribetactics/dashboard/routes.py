from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from tribetactics.users.utils import admin_required, restaurant_required
from tribetactics.dashboard.forms import RestaurantForm, ItemForm
from tribetactics.models import Item, Restaurant, Menu, Order
from tribetactics import db

dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/dashboard/')
@login_required
@restaurant_required
def restaurant_dash():
    return render_template('dashboard.html')


@dashboard.route('/dashboard/createRestaurant/', methods=['GET', 'POST'])
@login_required
@restaurant_required
def create_restaurant():
    form = RestaurantForm()
    if form.validate_on_submit():
        restaurant = Restaurant(name=form.name.data,
                    owner_id=current_user.id)
        db.session.add(restaurant)
        db.session.commit()
        menu = Menu(name=restaurant.name,
                    restaurant_id=restaurant.id)
        db.session.add(menu)
        db.session.commit()
        flash(f'Your account has been created', 'success')
        return redirect(url_for('dashboard.restaurant_dash'))
    return render_template('createRestaurant.html', title='Create Restaurant', form=form)

    
@dashboard.route('/dashboard/<int:id>/createItem/', methods=['GET', 'POST'])
@login_required
@restaurant_required
def create_item(id):
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(name=form.name.data,
                    price=form.price.data,
                    menu_id=id)
        db.session.add(item)
        db.session.commit()
        
        flash(f'Your item has been added!', 'success')
        return redirect(url_for('dashboard.restaurant_dash'))
    return render_template('createItem.html', title='Create Item', form=form)


@dashboard.route('/dashboard/editItem/<int:item_id>/', methods=['GET', 'POST'])
@login_required
@restaurant_required
def edit_item(item_id):
    form = ItemForm()
    item = Item.query.get(item_id)
    if item == None:
        flash(f'You entered wrong Item ID!', 'danger')
        return redirect(url_for('dashboard.restaurant_dash'))
    if form.validate_on_submit():
        item.name = form.name.data
        item.price = form.price.data
        db.session.commit()
        flash(f'Your item has been updated!', 'success')
        return redirect(url_for('dashboard.restaurant_dash'))
    return render_template('editItem.html', title='Edit Item', form=form, item=item)


@dashboard.route('/dashboard/deleteItem/<int:item_id>/')
@login_required
@restaurant_required
def delete_item(item_id):
    item = Item.query.get(item_id)
    if item == None:
        flash(f'this Item is not found', 'danger')
        return redirect(url_for('dashboard.restaurant_dash'))
    
    # print(item.orders[0].order.status)
    for itemOrder in item.orders:
        if itemOrder.order.status == 'Pending':
            flash(f'this Item is still in a pending order', 'danger')
            return redirect(url_for('dashboard.restaurant_dash'))
    db.session.delete(item)
    db.session.commit()
    flash(f'Your item has been deleted!', 'success')
    return redirect(url_for('dashboard.restaurant_dash'))


@dashboard.route('/dashboard/deleverOrder/<int:order_id>/')
@login_required
@restaurant_required
def deliver_order(order_id):
    order = Order.query.get(order_id)
    if order == None:
        flash(f'this order is not found', 'danger')
        return redirect(url_for('dashboard.restaurant_dash'))
    order.status = 'Delivered'
    db.session.commit()
    flash(f'Your order status has been updated!', 'success')
    return redirect(url_for('dashboard.restaurant_dash'))
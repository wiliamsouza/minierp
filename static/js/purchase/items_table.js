function addItem()
{
  tbodyNode = MochiKit.DOM.getElement('itemsTarget');
  supplier = MochiKit.DOM.getElement('id_supplier').value;
  product = MochiKit.DOM.getElement('id_product').value;
  quantity = MochiKit.DOM.getElement('id_quantity').value;
  cost = 10.50
  row = [product, quantity, cost, quantity*cost, INPUT({'type':'checkbox'})];
  tr = TR(null, MochiKit.Base.map(MochiKit.Base.partial(TD, null), row));
  MochiKit.DOM.appendChildNodes(tbodyNode, tr);
}
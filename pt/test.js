{/* <label class="mt-3" for="color">sizes / prices</label><br />

<div class="form-group mt-2">
  {% for size in size_data %}
  <div class="form-check">
    {% if size.name in l[0] %}
    <input class="form-check-input" value="{{size.name}}" type="checkbox" name="size"
      id="checkbox-{{size.name}}" checked  />
    <label class="form-check-label" for="checkbox-{{size.name}}">{{size.name}}</label>
    <input class="form-control" type="number" class="price" id="input-{{size.name}}"
      name="price" placeholder="Price" value="{{}}" />
      {% else %}
      <input class="form-check-input" value="{{size.name}}" type="checkbox" name="size"
        id="checkbox-{{size.name}}" 
         checked  />
      <label class="form-check-label" for="checkbox-{{size.name}}">{{size.name}}</label>
      <input class="form-control hidden-input" type="number" class="price" id="input-{{size.name}}"
        name="price" placeholder="Price" />
      {% endif %}
  </div>
  {% endfor %}
</div>
</div> */}

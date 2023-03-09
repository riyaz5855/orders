# summary page
@app.route('/summary', methods=['POST','GET'])
def summary():
    if request.method == 'POST':
        data=request.form.getlist('data')
        ddata=request.form.getlist('ddata')
        l=list(zip(data,ddata))
        grouped_data = {}
        for count, item in l:
            color = item.split("-")[0]  # extract the color from the item
            if color not in grouped_data:
                grouped_data[color] = []
            grouped_data[color].append((count, item))

        grouped_list = list(grouped_data.values())
        smry = [lst for lst in grouped_list if any(int(item[0]) > 0 for item in lst)]

    return render_template('summary.html',smry=smry)

<table>
  <thead>
    <tr>
      <th>color - price</th>
      {% for item in l[0] %}
        {% for size, price, hexcode in [(item[4], item[2], item[3])] %}
          <th>{{ size }} - {{ price }}</th>
        {% endfor %}
      {% endfor %}
    </tr>
  </thead>
  <tbody>
    {% for group in l %}
      {% for item in group %}
        <tr>
          <td>{{ item[1] }} - {{ item[2] }} - {{ item[3] }}</td>
          {% for size, _, _ in group[0] %}
            {% set quantity = '0' %}
            {% for i in group %}
              {% if i[4] == size %}
                {% set quantity = i[5] %}
              {% endif %}
            {% endfor %}
            <td>{{ quantity }}</td>
          {% endfor %}
        </tr>
      {% endfor %}
    {% endfor %}
  </tbody>
</table>

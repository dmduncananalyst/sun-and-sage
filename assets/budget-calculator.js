(() => {
  const form = document.getElementById('monthly-budget');
  if (!form) return;
  const inputs = [...form.querySelectorAll('[data-budget-field]')];
  const cents = input => Math.round(Math.max(0, Number(input.value) || 0) * 100);
  const money = value => (value / 100).toLocaleString('en-US', { style: 'currency', currency: 'USD' });
  function update() {
    const income = cents(inputs.find(input => input.dataset.budgetField === 'income'));
    const assigned = inputs.filter(input => input.dataset.budgetField !== 'income').reduce((sum, input) => sum + cents(input), 0);
    const balance = income - assigned;
    document.getElementById('budget-assigned').textContent = money(assigned);
    const label = document.getElementById('budget-balance-label');
    label.firstChild.textContent = balance < 0 ? 'Over your income by: ' : balance === 0 ? 'Every dollar assigned: ' : 'Money left to assign: ';
    document.getElementById('budget-balance').textContent = money(Math.abs(balance));
  }
  inputs.forEach(input => input.addEventListener('input', update));
  update();
})();

Here is the TypeScript React (TSX) code with inline comments to explain each section, function and important line of codes:

```tsx
export const Button = ({ label, onClick, disabled }) => { // Exporting a functional component as 'Button' that accepts three props : 'label', 'onClick' & 'disabled'.
  return (                                               // This is the main function where JSX returned by the button component.
    <button onClick={onClick} disabled={disabled}>       // Rendering a 'button' HTML element, with 'onClick' event listener and 'disabled' attribute based on props passed to Button component.
      {label}                                              // The label of the button will be whatever value is passed as prop 'label'.
    </button>                                             // JSX must always close its opening tag in a self-closing format like <Component /> or else it will throw an error.
  );
};
```

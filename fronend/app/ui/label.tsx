import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
// Label Component
  const Label = React.forwardRef<
    HTMLLabelElement,
    React.LabelHTMLAttributes<HTMLLabelElement>
  >(({ className, ...props }, ref) => {
    return (
      <label
        ref={ref}
        className={`text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 ${className}`}
        {...props}
      />
    )
  })
  Label.displayName = "Label"

  export { Label }
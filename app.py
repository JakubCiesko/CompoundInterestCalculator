import customtkinter # type: ignore
from tkinter import messagebox # type: ignore
from typing import Callable
from calculation import Calculation
PADX = 10
PADY = (10, 0)
position_arguments = {"padx": PADX, "pady":PADY}
FRAME_FG_COLOR = "#D1D5DE" #"#9DB5B2"
FONT_COLOR = "#353535"
READONLY_COLOR = "#B7B7B7"
NORMAL_COLOR = "#FFFFFF"
WINDOW_COLOR = "#FFFFFF" #"#DAF0EE"
BUTTON_COLOR = "#EAECF0"#"#00A896"##EAECF0
EXTRA_COLOR = "#202C39"
GLOBAL_FONT = ("Arial", 16)

def show_error_dialog(fn):
    def inner(*args, **kwargs):
        try: 
            output = fn(*args, **kwargs)
            return output
        except Exception as e: 
            print(e)
            messagebox.showerror("Error", e)
    return inner 

class InputFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=FRAME_FG_COLOR)
        self.variables = {
            "base": customtkinter.StringVar(),
            "monthly": customtkinter.StringVar(),
            "years": customtkinter.StringVar(),
            "interest": customtkinter.StringVar(),
            "final": customtkinter.StringVar(),
        }
        self.var_names_to_text = {
            "interest": "Interest",
            "base": "Base amount",
            "monthly": "Monthly contributions",
            "years": "Number of years",
            "final": "Final amount",
        }
        self.labels = []
        self.entries = {}
        for i, (var_name, var) in enumerate(self.variables.items()):
            label = customtkinter.CTkLabel(self, text=self.var_names_to_text[var_name], font=GLOBAL_FONT, text_color=FONT_COLOR)
            label.grid(row=i, column=0, sticky="w", **position_arguments)
            self.labels.append(label)
            entry = customtkinter.CTkEntry(self, textvariable=var, width=200, font=GLOBAL_FONT, text_color=FONT_COLOR)
            entry.grid(row=i, column=1, sticky="w", **position_arguments)
            self.entries[var_name] = entry
        self.entries["final"].configure(state="readonly", fg_color=READONLY_COLOR)
        

    def get_input(self, values=True):
        if values: 
            return {varname: varvalue.get() for varname, varvalue in self.variables.items()}
        return self.variables
    
    def set_readonly(self, *fields):
        for field in fields: 
            self.entries[field].delete(0, customtkinter.END)
            self.entries[field].configure(state="readonly", fg_color=READONLY_COLOR)
    
    def set_normal(self, *fields):
        for field in fields: 
            self.entries[field].configure(state="normal", fg_color=NORMAL_COLOR)
    

class OutputFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=FRAME_FG_COLOR)
        self.title = customtkinter.CTkLabel(self, text="Result", font=("Arial", 25), text_color=FONT_COLOR)
        self.title.grid(row=0, column=0, sticky="nw", **position_arguments)
        self.output = customtkinter.CTkEntry(self, width=400, font=GLOBAL_FONT, text_color=FONT_COLOR)
        self.output.configure(state="readonly")
        self.output.grid(row=1, column=0, sticky="nwse", **position_arguments)

    def display_text(self, text):
        self.output.configure(state="normal")
        self.output.delete(0, customtkinter.END)
        self.output.insert(0, text)
        self.output.configure(state="readonly")


class RadioButtonFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=FRAME_FG_COLOR)
        self.variable = customtkinter.IntVar()
        radiobutton_kwargs = {
            "variable":self.variable,
            "command":self.turnoff_entries,
            "font":GLOBAL_FONT,
            "text_color": FONT_COLOR,
            "fg_color": EXTRA_COLOR,
            "hover_color":EXTRA_COLOR,
        }
        self.final_amount_radio = customtkinter.CTkRadioButton(self, text="Final amount", value=0, **radiobutton_kwargs)
        self.final_amount_radio.grid(row=0, column=0, sticky="w", **position_arguments)
        self.monthly_contribution_radio = customtkinter.CTkRadioButton(self, text="Monthly contribution", value=1, **radiobutton_kwargs)
        self.monthly_contribution_radio.grid(row=1, column=0, sticky="w", **position_arguments)
        self.base_amount_radio = customtkinter.CTkRadioButton(self, text="Base amount", value=2, **radiobutton_kwargs)
        self.base_amount_radio.grid(row=2, column=0, sticky="w", **position_arguments)
        self.button = customtkinter.CTkButton(self, text="Calculate", command=self.process_input, fg_color=BUTTON_COLOR, font=GLOBAL_FONT, text_color=FONT_COLOR, hover_color=BUTTON_COLOR)
        self.button.place(relx=0.5, rely=0.75, anchor=customtkinter.CENTER)
    
    @show_error_dialog
    def process_input(self):
        use_case_index = self.variable.get()
        input = self.master.input_frame.get_input()
        input["p_a"] = input.pop("interest")
        to_float = lambda str: float(str) if str else 0.0
        to_int = lambda str: int(str) if str else 0
        input = self.change_input_type(input, {
            "p_a": to_float,
            "base": to_float,
            "monthly": to_float,
            "years": to_int,
            "final": to_float,
        })
        calculation = Calculation(use_case_index)
        output = calculation(**input)
        self.show_result(output)
    
    def show_result(self, result):
        self.master.output_frame.display_text(result)
        
    def change_input_type(self, input: dict, varname_vartype:dict[str, Callable]):
        transformed_input = {}
        for var_name, value in input.items():
            enforce_type = varname_vartype[var_name]
            #try: 
            transformed_input[var_name] = enforce_type(value)
            #except Exception as e: 
            #    print(e)
            #    messagebox.showerror("Error", "Something went wrong.")
        return transformed_input
    
    def turnoff_entries(self):
        input_frame = self.master.input_frame
        input_frame.set_normal("interest", "base", "monthly", "years", "final")
        selected_value = self.variable.get()
        match selected_value:
            case 0:
                input_frame.set_readonly("final")
            case 1:
                input_frame.set_readonly("monthly")
            case 2:
                input_frame.set_readonly("base")
    
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Interest calculator")
        self.geometry("800x800")
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((0,1), weight=1)
        self.configure(fg_color=WINDOW_COLOR)
        self.input_frame = InputFrame(self)
        self.input_frame.grid(row=0, column=0, sticky="nswe", **position_arguments)
        self.radiobutton_frame = RadioButtonFrame(self)
        self.radiobutton_frame.grid(row=0, column=1, sticky="nswe", **position_arguments)
        self.output_frame = OutputFrame(self)
        self.output_frame.grid(row=1, column=0, columnspan=2, sticky="nswe", **position_arguments)


        
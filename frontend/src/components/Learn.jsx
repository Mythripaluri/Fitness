import { CheckCircle2 } from "lucide-react";
import { trainingOptions } from "../constants";
const Learn = () => {
  return (
    <div className="mt-10">
      <h2 className="text-3xl sm:text-5xl lg:text-6xl text-center my-8 tracking-wide">
        Learn🏋️
      </h2>
      <div className="flex flex-wrap">
        {trainingOptions.map((option,index) => (
            <div key={index} className="w-full sm:w-1/2 lg:w-1/3 p-2">
                <div className="p-10 border border-neutral-700 rounded-xl">
                    <p className="text-4xl mb-8">
                        {option.title}
                        {option.title == "Mediocre"}
                    </p>
                    <ul>
                        {option.exercises.map((exercise, index) => (
                            <li key={index} className="mt-8 flex items-center">
                               <CheckCircle2 />
                               <span className="ml-2">{exercise}</span> 
                            </li>
                        ))}
                    </ul>
                    <a href="#" className="inline-flex justify-center items-center text-center w-full h-12 p-5 mt-20 tracking-tight text-xl sm:hover:bg-cyan-900 border border-cyan-900 rounded-lg transition duration-200">Try Now!</a>
                </div>
            </div>
        ))}
      </div>
    </div>
  )
}

export default Learn

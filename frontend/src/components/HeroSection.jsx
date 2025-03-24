const HeroSection = () => {
    return (
        <div className="flex flex-col items-center mt-11 lg:mt-18">
            <h1 className="text-4xl sm:text-6xl lg:text-7xl text-center tracking-wide">
                <span className="bg-gradient-to-r from-cyan-600 to-cyan-900 text-transparent bg-clip-text">
                    FitLens
                </span><br />
                &nbsp; Your AI-Powered Fitness Coach
            </h1>

            <p className="mt-8 text-lg text-center text-neutral-400 max-w-4xl">
                Train smarter with real-time posture detection and AI-guided corrections.
                Enhance your workouts, prevent injuries, and achieve better results with
                personalized feedback for every rep.
            </p>

            <div className="flex justify-center my-8">
                <a href="#" className="bg-gradient-to-r from-cyan-600 to-cyan-900 py-3 px-4 mx-3 rounded-md">
                    Start Your AI Training
                </a>
            </div>

            <div className="flex mt-10 justify-center gap-14">
                <video autoPlay loop muted 
                    className="rounded-lg w-[50%] md:w-[45%] lg:w-[400px] h-[120px] md:h-[150px] lg:h-[230px] border-[2px] md:border-[3px] lg:border-[4px] border-cyan-500 shadow-sky-200 object-cover">
                    <source src="/fit3.mp4" type="video/mp4" />
                    Your browser does not support the video tag.
                </video>
                <video autoPlay loop muted 
                    className="rounded-lg w-[50%] md:w-[45%] lg:w-[400px] h-[120px] md:h-[150px] lg:h-[230px] border-[2px] md:border-[3px] lg:border-[4px] border-cyan-500 shadow-sky-200 object-cover">
                    <source src="/fit2.mp4" type="video/mp4" />
                    Your browser does not support the video tag.
                </video>
            </div>
        </div>
    );
}

export default HeroSection;

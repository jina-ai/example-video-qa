type AboutPoint = string | React.ReactNode

const About = ({aboutPoints, className}: { aboutPoints: AboutPoint[], className?: string }) => {
    return (
        <div className={className}>
            <h2 className="font-bold text-xl mb-3">
                About
            </h2>
            <ul>
                {aboutPoints.map((aboutPoint, index) => <li key={`aboutPoint-${index}`} className="ml-3 mb-3 text-gray-600">• {aboutPoint}</li>)}
            </ul>
        </div>
    );
};

export default About
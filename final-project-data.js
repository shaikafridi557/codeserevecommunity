// Final Project Data for Portfolio Addition
// This data structure contains all prepared content for both new projects

const newProjects = [
  {
    id: "sireeshna-solutions",
    title: "Sireeshna Solutions",
    category: "IT Services Platform",
    challenge: "An IT services company needed a comprehensive platform to showcase their training programs, job placement services, and visa processing capabilities in Vijayawada.",
    solution: "We developed a professional website highlighting their IT services, training programs in Vijayawada, and global career opportunities, establishing their digital presence in the competitive IT services market.",
    imageUrl: "https://images.pexels.com/photos/3184465/pexels-photo-3184465.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
    projectUrl: "https://sireeshnasolutions.com/",
    altText: "Sireeshna Solutions IT Services Platform",
    overlay: "4" // Consistent with existing projects
  },
  {
    id: "dr-kammela-medical",
    title: "Dr. Kammela Medical Center",
    category: "Healthcare Website",
    challenge: "A renowned medical specialist needed a professional online presence to showcase expertise in kidney treatments, robotic surgery, and IVF services.",
    solution: "We created a comprehensive medical website featuring the doctor's credentials, specializations, and appointment services, enhancing patient accessibility and trust in healthcare services.",
    imageUrl: "https://images.pexels.com/photos/236380/pexels-photo-236380.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
    projectUrl: "https://drkammelasreedharvundavallisridevikidneyandrogyivf.com/",
    altText: "Dr. Kammela Medical Center Website",
    overlay: "4" // Consistent with existing projects
  }
];

// Schema.org structured data additions
const schemaAdditions = [
  {
    "@type": "WebSite",
    "name": "Sireeshna Solutions",
    "description": "IT services and training platform",
    "url": "https://sireeshnasolutions.com/"
  },
  {
    "@type": "WebSite", 
    "name": "Dr. Kammela Medical Website",
    "description": "Medical specialist website for kidney and IVF services",
    "url": "https://drkammelasreedharvundavallisridevikidneyandrogyivf.com/"
  }
];

// Export for use in implementation
module.exports = { newProjects, schemaAdditions };
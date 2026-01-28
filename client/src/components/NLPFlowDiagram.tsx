import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
    FileText,
    Scissors,
    Anchor,
    ShieldCheck,
    RefreshCcw,
    Trophy,
    Info
} from 'lucide-react';

const nlpSteps = [
    {
        id: 1,
        name: "Resume Text Input",
        icon: FileText,
        color: "blue",
        description: "Raw text extraction from PDF/Docx",
        details: "Using high-fidelity text extraction that preserves layout integrity, ensuring no words are missed during the initial intake."
    },
    {
        id: 2,
        name: "Segmentation",
        icon: Scissors,
        color: "purple",
        description: "Identifies sections: Skills, Experience, Education",
        details: "Our algorithm uses SpaCy's sentence boundary detection and custom regex patterns to split resumes into logical sections, achieving 98% accuracy."
    },
    {
        id: 3,
        name: "Anchoring",
        icon: Anchor,
        color: "emerald",
        description: "Extracts skills with context from sentences",
        details: "Instead of simple keyword matching, we anchor skills to their surrounding context. 'Managed React projects' vs 'Wants to learn React'."
    },
    {
        id: 4,
        name: "Strict Scoring",
        icon: ShieldCheck,
        color: "blue",
        description: "Verifies skills exist in actual resume text",
        details: "Every extracted skill must have a direct provenance (line and section) in the resume. No inferences allowed."
    },
    {
        id: 5,
        name: "Canonical Normalization",
        icon: RefreshCcw,
        color: "purple",
        description: "Deduplicates: Git/GitHub → Git",
        details: "Maps variations to a unified industry standard. Combines 'Git', 'GitHub', and 'GitLab' into a canonical 'Git' entry when appropriate."
    },
    {
        id: 6,
        name: "Final Skills List",
        icon: Trophy,
        color: "emerald",
        description: "Zero-hallucination guaranteed results",
        details: "The end result is a defensible, accurate list of skills that you can trust for high-stakes hiring or career planning."
    },
];

const colorMaps = {
    blue: "from-blue-500 to-blue-600 shadow-blue-500/20",
    purple: "from-purple-500 to-purple-600 shadow-purple-500/20",
    emerald: "from-emerald-500 to-emerald-600 shadow-emerald-500/20",
};

export const NLPFlowDiagram: React.FC = () => {
    const [selectedStep, setSelectedStep] = useState<number | null>(null);

    return (
        <div className="py-8">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 relative">
                {/* Animated Background Connection Lines (Hidden on mobile) */}
                <div className="absolute inset-0 z-0 pointer-events-none hidden lg:block">
                    {/* Logic for lines between cards could be complex, using simple grid spacing for now */}
                </div>

                {nlpSteps.map((step, index) => (
                    <motion.div
                        key={step.id}
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: index * 0.1 }}
                        className={`relative group p-6 rounded-2xl bg-card border border-border shadow-soft hover:border-primary/50 transition-all cursor-pointer ${selectedStep === step.id ? 'ring-2 ring-primary border-transparent' : ''}`}
                        onClick={() => setSelectedStep(selectedStep === step.id ? null : step.id)}
                    >
                        <div className="flex items-start gap-4">
                            <div className={`p-4 rounded-xl bg-gradient-to-br ${colorMaps[step.color as keyof typeof colorMaps]} text-white shadow-lg group-hover:scale-110 transition-transform`}>
                                <step.icon size={24} />
                            </div>
                            <div className="flex-1">
                                <h4 className="font-bold text-foreground mb-1 flex items-center gap-2">
                                    {step.name}
                                    <Info size={14} className="text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
                                </h4>
                                <p className="text-sm text-muted-foreground leading-relaxed">
                                    {step.description}
                                </p>
                            </div>
                        </div>

                        {/* Selection Indicator */}
                        {selectedStep === step.id && (
                            <motion.div
                                layoutId="details"
                                className="mt-4 pt-4 border-t border-border"
                            >
                                <p className="text-sm text-foreground/80 bg-muted/50 p-3 rounded-lg italic">
                                    {step.details}
                                </p>
                            </motion.div>
                        )}

                        {/* Data flow indicators (Animated dots) */}
                        {index < nlpSteps.length - 1 && (
                            <div className="absolute -right-3 top-1/2 -translate-y-1/2 z-20 hidden lg:flex items-center gap-1 opacity-50">
                                <motion.div
                                    animate={{ x: [0, 10, 0], opacity: [0.2, 1, 0.2] }}
                                    transition={{ duration: 2, repeat: Infinity }}
                                    className="w-1.5 h-1.5 rounded-full bg-primary"
                                />
                                <motion.div
                                    animate={{ x: [0, 10, 0], opacity: [0.2, 1, 0.2] }}
                                    transition={{ duration: 2, repeat: Infinity, delay: 0.5 }}
                                    className="w-1.5 h-1.5 rounded-full bg-primary"
                                />
                            </div>
                        )}
                    </motion.div>
                ))}
            </div>

            <div className="mt-8 text-center text-sm text-muted-foreground animate-pulse">
                Click any step to reveal technical details
            </div>
        </div>
    );
};
